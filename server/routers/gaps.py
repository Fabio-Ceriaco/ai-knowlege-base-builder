"""
Gaps router - surfaces knowledge base coverage gaps.

Gap rows are created by POST /ask when max_similarity < 0.80.
This router lets consumers retrieve and triage those gaps.

Endpoints:

    GET /gaps - list all unreviewed gaps
    PATCH /gaps/{id}/reviewed - mark a gap as reviewed
"""

from fastapi import APIRouter, HTTPException
from server.database import get_cursor

router = APIRouter()


# --- GET /gaps ---


@router.get("/gaps")
def list_gaps():
    """
    Return all unreviewd coverage gaps, newest first.

    Each row contains:
        - id: gap primary key
        - question_id: FK to question_log
        - question: the original question text
        - max_similarity: best cosine score found (below 0.80)
        - gap_topic: Claude-inferred topic label (may be null)
        - created_at: when the gap was detected
    """

    try:
        with get_cursor(commit=False) as cur:
            cur.execute("""
                    SELECT 
                        id,
                        question_id,
                        question,
                        max_similarity,
                        gap_topic,
                        created_at
                    FROM coverage_gaps
                    WHERE reviewed = FALSE
                    ORDER BY created_at DESC
                """)

            rows = cur.fetchall()

            # --- Format for JSON response ---
            # RealDictCursor returns dicts, but we still need to
            # handle datetime serialization for created_at
            gaps = []

            for row in rows:
                gaps.append(
                    {
                        "id": row["id"],
                        "question_id": row["question_id"],
                        "question": row["question"],
                        "max_similarity": (
                            float(row["max_similarity"])
                            if row["max_similarity"] is not None
                            else None
                        ),
                        "gap_topic": row["gap_topic"],
                        "created_at": (
                            row["created_at"].isoformat() if row["created_at"] else None
                        ),
                    }
                )
            return {"total_unreviewed": len(gaps), "gaps": gaps}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch gaps: {str(e)}")


# --- PATCH /gaps/{id}/reviewed ---
@router.patch("/gaps/{gap_id}/reviewed")
def mark_gap_reviewed(gap_id: int):
    """
    Mark a single coverage gap as reviewed.

    Returns 404 if the gap_id doesn't exist, which protects
    against stale Retool dashboard state (e.g., two users
    triaging the same gap simultaneously).
    """
    try:
        with get_cursor(commit=True) as cur:
            # --- Update and check rowcount ---
            # Using RETURNING avoids a second SELECT to confirm
            # the row existed. If no row comes back, it's a 404
            cur.execute(
                """
                    UPDATE coverage_gaps
                    SET reviewed = TRUE
                    WHERE id = %s AND reviewed = FALSE
                    RETURNING id, question
                """,
                (gap_id,),
            )

            result = cur.fetchone()

        if not result:
            # Could be: (a) gap_id doesn't exist or
            # (b) it was already reviewed. Either way, nothing to do
            raise HTTPException(
                status_code=404, detail=f"Gap {gap_id} not found or already reviewed."
            )

        return {
            "message": "Gap marked as reviewed.",
            "gap_id": result["id"],
            "question": result["question"],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update gap: {str(e)}")
