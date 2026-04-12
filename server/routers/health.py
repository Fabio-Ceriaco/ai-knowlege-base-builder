"""GET /health - public liveness check."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    """
    Returns immediatly with no side effects.

    Deliberately does NOT check the database - this endpoint answers
    "is the process alive?" not "is the whole system healthy?". Mixing
    the two gives flapping alarms when the DB has a 2-sec hiccup.
    """

    return {"status": "ok"}
