"""Semantic search over document chunks using pgvector cosin similarity."""

import os
import logging
from dotenv import load_dotenv
from server.database import get_cursor
from server.services.embedder import embed_single

load_dotenv()

logger = logging.getLogger(__name__)

# Top-K chunks to retrieve. Read from env so it's tunable without code changes.

TOP_K = int(os.getenv("TOP_K", 5))


def retrieve_chunks(question: str) -> dict:
    """
    Embed a question and find the most similar document chunks.

    Pipeline:
        1. Embed the question using Voyage (input_type="query")
        2. Run pgvector cosine distance search across all chunks
        3. Convert distance to similarity (1 - distance)
        4. Return ranked chunks + metadata

    Return a dict instead of just a list of chunks:
        - The /ask endpoint needs max_similarity for gap detection
        - The question_log table needs chunks_ids for audit
        - Bundling everything in one return avoids the caller
            re-computing these values from the raw list

    Args:
        question: The user's natural language question


    Returns:
        dict with keys:
            - chunks: list of dicts (id, document_id, chunk_index, chunk_text,
            token_count, similarity, document_title)
            - chunk_ids: list of chunk IDs used (for questions_log)
            - max_similarity: highest similarity score (for gap detection)
            - top_k: how many chunks were requested
    """

    # --- Embed the question ---
    # input_type = "query" is critical - Voyage uses asymmetric embeddings.
    # A query embedding is optimized to match against document embeddings,
    # not against other queries.
    logger.info(f"Embedding question: '{question[:80]}...'")
    question_embedding = embed_single(question, input_type="query")

    # --- pgvector cosine distance search ---
    # The <=> operator computes cosine distance (1 - similarity).
    # We JOIN documents to get the title for source citations.
    # ORDER BY distance ASC
    with get_cursor(commit=False) as cur:
        cur.execute(
            """
                SELECT
                    c.id,
                    c.document_id,
                    c.chunk_index,
                    c.chunk_text,
                    c.token_count,
                    c.embedding <=> %s::vector AS distance,
                    d.title AS document_title
                FROM document_chunks c
                JOIN documents d ON d.id = c.document_id
                ORDER BY distance ASC
                LIMIT %s
            """,
            (question_embedding, TOP_K),
        )
        rows = cur.fetchall()

    # --- Convert distance -> similarity and build result
    chunks = []
    for row in rows:
        chunks.append(
            {
                "id": row["id"],
                "document_id": row["document_id"],
                "chunk_index": row["chunk_index"],
                "chunk_text": row["chunk_text"],
                "token_count": row["token_count"],
                "similarity": round(1 - float(row["distance"], 4)),
                "document_title": row["document_title"],
            }
        )
    chunk_ids = [c["id"] for c in chunks]
    max_similarity = chunks[0]["similarity"] if chunks else 0.0

    logger.info(
        f"Retrieved {len(chunks)} chunks - "
        f"max_similarity={max_similarity:.4f}, "
        f"chunk_ids={chunk_ids}"
    )

    return {
        "chunks": chunks,
        "chunk_ids": chunk_ids,
        "max_similarity": max_similarity,
        "top_k": TOP_K,
    }
