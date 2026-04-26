"""POST /ask - RAG query: embed question, retrieve chunks, generate answer."""

import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from server.database import get_cursor
from server.services.retriever import retrieve_chunks
from server.services.generator import generate_answer
from server.utils.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# --- Gap threshold from enviorment - if max_similerity is blow this,
# the knowledge base doesn't adequately cover the topic.

GAP_THRESHOLD = float(settings.GAP_THRESHOLD)


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="The natural language question to answer.",
    )


@router.post("/ask")
def ask(payload: AskRequest):
    """
    Full RAG query pipeline:
    1. Retrieve top-k chunks via semantic search
    2. Generate answer via Claude with chunk context
    3. Detect coverage gap (max_similarity < threshold)
    4. Log questions + answers to questions_log
    5. If gap detected, write to coverage_gaps
    6. Return answer + sources + metadata
    """

    question = payload.question.strip()

    # --- Retrieve relevant chunks --

    try:
        retrieval = retrieve_chunks(question)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Retrieval failed: {str(e)}")

    chunks = retrieval["chunks"]
    max_similarity = retrieval["max_similarity"]
    chunks_ids = retrieval["chunks_ids"]

    # Edge case: no chunks in the database at all
    if not chunks:
        raise HTTPException(
            status_code=404,
            detail="No document chunks found. Ingest documents before asking questions",
        )

    # --- Generate answer via Claude ---

    try:
        answer_data = generate_answer(question, chunks)
    except Exception as e:
        raise HTTPException(
            status_code=503, detail=f"Answer generation failed: {str(e)}"
        )

    # --- Gap detection ---

    is_gap = max_similarity < GAP_THRESHOLD

    # --- Log to questions_log ---

    try:
        question_id = _log_question(
            question=question,
            answer=answer_data["answer"],
            chunk_ids=chunks_ids,
            max_similarity=max_similarity,
            is_gap=is_gap,
            model_used=answer_data["model_used"],
            response_ms=answer_data["response_ms"],
        )
    except Exception as e:
        logger.error(f"Failed to log question: {str(e)}")
        question_id = None

    # --- If gap, write to coverage_gaps ---

    if is_gap and question_id:
        try:
            _log_gap(
                question_id=question_id,
                question=question,
                max_similarity=max_similarity,
            )
        except Exception as e:
            logger.error(f"Failed to log coverage gap: {str(e)}")

    # --- Build response ---

    sources = [
        {
            "chunk_id": c["id"],
            "document_title": c["document_title"],
            "chunk_index": c["chunk_index"],
            "similarity": c["similarity"],
            "chunk_text": (
                c["chunk_text"][:200] + "..."
                if len(c["chunk_text"]) > 200
                else c["chunk_text"]
            ),
        }
        for c in chunks
    ]

    return {
        "answer": answer_data["answer"],
        "confidence": answer_data["confidence"],
        "is_answerable": answer_data["is_answerable"],
        "cited_chunks": answer_data["cited_chunks"],
        "sources": sources,
        "max_similarity": max_similarity,
        "is_gap": is_gap,
        "question_id": question_id,
        "model_used": answer_data["model_used"],
        "response_ms": answer_data["response_ms"],
    }


def _log_question(
    question: str,
    answer: str,
    chunk_ids: list,
    max_similarity: float,
    is_gap: bool,
    model_used: str,
    response_ms: int,
) -> int:
    """
    Write one row to questions_log. Returns the new row's id.

    Keeps the main endpoint readable and the DB logic isolated.
    """
    with get_cursor(commit=True) as cur:
        cur.execute(
            """
                INSERT INTO questions_log
                    (question, answer, chunks_ids, max_similarity, is_gap, model_used, response_ms)
                VALUES
                    (%s,%s,%s,%s,%s,%s,%s)
                RETURNING id
            """,
            (
                question,
                answer,
                chunk_ids,
                max_similarity,
                is_gap,
                model_used,
                response_ms,
            ),
        )
        return cur.fetchone()["id"]


def _log_gap(question_id: int, question: str, max_similarity: float):
    """
    Write one row to coverage_gaps when a question hits below the threshold.

    gap_topic add Claude-inferred topic clustering to automatically label what subject area the gap falls in.

    """
    with get_cursor(commit=True) as cur:
        cur.execute(
            """
                INSERT INTO coverage_gaps 
                    (question_id, question, max_similarity)
                VALUES (%s, %s, %s)
            """,
            (question_id, question, max_similarity),
        )
    logger.info(
        f"Coverage gap logged - question_id={question_id}, "
        f"max_similarity={max_similarity:.4f}"
    )
