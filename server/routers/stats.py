"""GET /stats - authenticated counts of KB state."""

from fastapi import APIRouter
from server.database import get_cursor

router = APIRouter()


@router.get("/stats")
def stats():
    """
    Returns current counts: documents, chunks, unreviewed gaps, total questions.
    """

    with get_cursor() as cur:
        cur.execute("SELECT COUNT(*) AS n FROM documents")
        documents = cur.fetchone()["n"]

        cur.execute("SELECT COUNT(*) AS n FROM document_chunks")
        chunks = cur.fetchone()["n"]

        cur.execute("SELECT COUNT(*) AS n FROM coverage_gaps WHERE reviewed = FALSE")
        open_gaps = cur.fetchone()["n"]

        cur.execute("SELECT COUNT(*) AS n FROM questions_log")
        questions_asked = cur.fetchone()["n"]

        return {
            "doduments": documents,
            "chunks": chunks,
            "open_gaps": open_gaps,
            "questions_asked": questions_asked,
        }
