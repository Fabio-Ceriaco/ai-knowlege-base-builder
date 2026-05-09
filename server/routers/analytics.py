"""GET /analytics/* - Aggregated metrics for the Analytics dashboard view."""

import logging
from fastapi import APIRouter, HTTPException
from server.database import get_cursor

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/questions-per-day")
def questions_per_day():
    """
    Return count of questions asked, grouped by calendar day.

    DATE(asked_at):
        asked_at is TIMESTAMPTZ - truncating to DATE collapses all questions
        from the same day into one row, giving us time-series shape
        the line chart needs.

    Returns last 30 days only - older data isn't useful for trend display
    and keeps tha chart readable.
    """

    try:
        with get_cursor() as cur:
            cur.execute("""
                    SELECT
                        DATE(asked_at) AS day,
                        count(*) AS question_count
                    FROM questions_log
                    WHERE asked_at >= NOW() - INTERVAL '30 days'
                    GROUP BY DATE(asked_at)
                    ORDER BY day ASC
                """)

            rows = cur.fetchall()
        return {
            "data": [
                {"day": str(row["day"]), "question_count": row["question_count"]}
                for row in rows
            ]
        }
    except Exception as e:
        logger.error(f"questions-per-day query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analytics query failed: {str(e)}")


@router.get("/gap-topics")
def gap_topics():
    """
    Return count of gaps grouped by gap_topic, descending.


    Only unrevised gaps - reviewed gaps are closed issues, not
    actionable knowledge base weaknesses.
    """
    try:
        with get_cursor() as cur:
            cur.execute("""
                    SELECT
                        COALESCE(gap_topic, 'Uncategorized') AS topic,
                        COUNT(*) as gap_count
                    FROM coverage_gaps
                    WHERE reviewed = FALSE
                    GROUP BY COALESCE(gap_topic, 'Uncategorized')
                    ORDER BY gap_count DESC
                    LIMIT 10
                """)
            rows = cur.fetchall()

        return {
            "data": [
                {"topic": row["topic"], "gap_count": row["gap_count"]} for row in rows
            ]
        }
    except Exception as e:
        logger.error(f"gap-topic query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analytics query failed: {str(e)}")


@router.get("/similarity-trend")
def similarity_trend():
    """
    Return average max_similarity score grouped by day.

    A rising average similarity trend means that KB is getting better
    coverage - questions are finding closer matches. A falling trend
    means users are asking about topics that KB hadn't ingested yet.

    ROUND(..., 4) matches the NUMERIC(6,4) precision of the column
    so values are consistent between raw DB reads and this endpoint.
    """

    try:
        with get_cursor() as cur:
            cur.execute("""
                    SELECT
                        DATE(asked_at) AS day,
                        ROUND(AVG(max_similarity)::NUMERIC, 4) AS avg_similarity
                    FROM questions_log
                    WHERE asked_at >= NOW() - INTERVAL '30 days'
                    GROUP BY DATE(asked_at)
                    ORDER BY day ASC
                """)

            rows = cur.fetchall()

        return {
            "data": [
                {"day": str(row["day"]), "avg_similarity": float(row["avg_similarity"])}
                for row in rows
            ]
        }
    except Exception as e:
        logger.error(f"similarity-trend query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analytics query failed. {str(e)}")


@router.get("/top-documents")
def top_documents():
    """
    Return documents ranked by how many times their chunks were used
    to answer questions.

    UNNEST:
        questions_log.chunks_ids is INTEGER[] - each row contains an array
        of chunks IDs used to answer that questions. UNNEST expands each array
        into individual rows so we can JOIN against document_chunks and then
        documents to get the title.

    This tells which documents are doing the most work in KB - useful for knowing what to keep updated.
    """
    try:
        with get_cursor() as cur:
            cur.execute("""
                    SELECT 
                        d.title AS document_title,
                        COUNT(*) AS usage_count
                    FROM questions_log ql
                    CROSS JOIN UNNEST(ql.chunks_ids) AS chunk_id
                    JOIN document_chunks dc ON dc.id = chunk_id
                    JOIN documents d ON d.id = dc.document_id
                    GROUP BY d.title
                    ORDER BY usage_count DESC
                    LIMIT 10
                """)

            rows = cur.fetchall()
        return {
            "data": [
                {
                    "document_title": row["document_title"],
                    "usage_count": row["usage_count"],
                }
                for row in rows
            ]
        }
    except Exception as e:
        logger.error(f"top-document query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analytics query failed: {str(e)}")
