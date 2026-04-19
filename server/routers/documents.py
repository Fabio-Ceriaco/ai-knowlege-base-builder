"""
GET /documents - list all documents (with optional status filter)
DELETE /documents/{id} - hard-delete a document and its cascaded chunks

"""

from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional

from server.database import get_cursor


router = APIRouter()


@router.get("/documents")
def list_documents(
    status: Optional[str] = Query(
        None, description="Filter by status: 'active' or 'archived'"
    )
):
    """
    Return all documents ordered by most recently ingested first.

    Optional query param ?status= active or ?status=archived filters the list.
    Without it, all documents are returned regardless of status.
    """

    # --- Validate the status filter if provided ---
    # Whitelist approach: only allow know values. This prevents SQL injection
    # even though we use parameterized queris (belt + suspenders), and also
    # gives the caller a clear error instead of an emprty result set when they
    # typo 'actve'IsADirectoryError

    VALID_STATUSES = {"active", "archived"}
    if status is not None and status not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status '{status}'. Must be one of: {', '.join(VALID_STATUSES)}",
        )
    with get_cursor(commit=False) as cur:
        if status:
            cur.execute(
                """
                    SELECT 
                        id,
                        title,
                        source_type,
                        file_name,
                        file_size_bytes,
                        chunk_count,
                        ingested_at,
                        updated_at,
                        status
                    FROM documents
                    WHERE status = %s
                    ORDER BY ingested_at DESC
                """,
                (status,),
            )
        else:
            cur.execute(
                """
                    SELECT 
                        id,
                        title,
                        source_type,
                        file_name,
                        file_size_bytes,
                        chunk_count,
                        ingested_at,
                        updated_at,
                        status
                    FROM documents
                    ORDER BY ingested_at DESC
                """
            )

        documents = cur.fetchall()
    return {"documents": documents, "count": len(documents)}


@router.delete("/documents/{document_id}")
def delete_document(document_id: int):
    """
    Hard-deletes a document and all its chunks (via ON DELETE CASCADE).

    Returns the deleted document's metadata so the caller can confirm
    what was removed. Returns 404 if the document doesn't exist.

    Example:

        DELETE /documents/123
    """

    # --- Verify the document exists and capture its metadata ---
    with get_cursor(commit=False) as cur:
        cur.execute(
            """
                SELECT 
                    id,
                    title,
                    source_type,
                    file_name,
                    chunk_count,
                    ingested_at,
                    status
                FROM documents
                WHERE id = %s
            """,
            (document_id,),
        )

        document = cur.fetchone()
    if not document:
        raise HTTPException(
            status_code=404,
            detail=f"Document with id={document_id} not found.",
        )

    # --- Delete the document and its chunks ---
    with get_cursor(commit=True) as cur:
        cur.execute(
            """
                DELETE FROM documents WHERE id = %s
            """,
            (document_id,),
        )
    return {
        "deleted": True,
        "document": document,
    }
