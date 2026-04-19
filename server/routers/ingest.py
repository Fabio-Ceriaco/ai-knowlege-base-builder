"""POST /ingest - upload a document, extract, chunk, embed, store."""

import os
from pathlib import Path
from fastapi import APIRouter, File, HTTPException, UploadFile

from server.database import get_cursor
from server.services.extractor import extract_text
from server.services.chunker import chunk_text
from server.services.embedder import embed_texts

router = APIRouter()

# --- Allowed file extentions ---

ALLOWED_EXTENSIONS = {".pdf", ".md", ".txt"}

# --- Upload directaory ---
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    """
    Full ingestion pipeline:
    1. Validate file type
    2. Save to disk temporarily
    3. Extract text
    4. Chunk text (1024 tokens, 128 overlap)
    5. Embed all chunks (Voyage, voyage-3.5)
    6. Write document + chunks to database
    7. Return metadata
    """

    # --- Validate file type ---
    file_name = file.filename or "Unknown"
    extension = Path(file_name).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{extension}'. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    # --- Save file to disk ---
    file_path = UPLOAD_DIR / file_name
    try:
        contents = await file.read()

        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        return HTTPException(
            status_code=500, detail=f"Failed to save uploaded file: {str(e)}"
        )
    if not contents:
        raise HTTPException(
            status_code=400,
            detail=f"Uploaded file '{file_name}' is empty.",
        )

    # --- Extract text ---
    try:
        text = extract_text(
            file_bytes=contents, file_name=file_name, content_type=file.content_type
        )

        if not text["text"] or not text["text"].strip():
            raise HTTPException(
                status_code=400,
                detail=f"No text content could be extracted from '{file_name}'.",
            )

        # --- Chunk text ---
        chunks = chunk_text(text["text"])
        if not chunks:
            raise HTTPException(
                status_code=400,
                detail=f"Text extracted but produced zero chunks from '{file_name}'.",
            )
        try:

            # --- Embed all chunks ---
            embeddings = embed_texts(
                [c["chunk_text"] for c in chunks], input_type="document"
            )
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Embedding failed: {str(e)}.")

            # Defensive check: embedding count must match chunk count.
            # If the embedder silently dropped a chunk (API error, empty text),
            # inserting misaligned data would corrupt the knowledge base.

        if len(embeddings) != len(chunks):
            raise HTTPException(
                status_code=500,
                detail=f"Embedding count mismatch: {len(chunks)} chunks but {len(embeddings)} embeddings.",
            )

        # --- Insert into database ---
        title = Path(file_name).stem  # e.g. fastapi.md -> fastapi
        document_id = _store_document_and_chunks(
            title=title,
            source_type=text["source_type"],
            file_name=file_name,
            file_size_bytes=text["file_size_bytes"],
            chunks=chunks,
            embeddings=embeddings,
        )

        return {
            "document_id": document_id,
            "title": title,
            "source_type": text["source_type"],
            "file_name": file_name,
            "file_size_bytes": text["file_size_bytes"],
            "chunk_count": len(chunks),
        }
    finally:
        # --- Cleanup: remove the temporary file ---
        # Runs whether the pipeline succeeded or failed.
        # The file served its purpose during extraction — keeping it
        # wastes disk and creates stale data if the same filename is
        # re-uploaded later.
        if file_path.exists():
            os.remove(file_path)


def _store_document_and_chunks(
    title: str,
    source_type: str,
    file_name: str,
    file_size_bytes: int,
    chunks: list,
    embeddings: list,
) -> int:
    """
    Inserts one document row + all its chunk rows in a single transaction.

    1. The ingest endpoint stays readable — the pipeline steps are clear
    2. The DB logic is testable in isolation if we ever need to
    3. The transaction boundary is explicit — one get_cursor(commit=True)
       wraps the entire write

    Returns the new document's id.
    """

    with get_cursor() as cur:
        # Insert document metadata
        cur.execute(
            """
                INSERT INTO documents (title, source_type, file_name, file_size_bytes, chunk_count)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """,
            (title, source_type, file_name, file_size_bytes, len(chunks)),
        )

        document_id = cur.fetchone()["id"]

        # Insert all chunks with their embeddings
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            cur.execute(
                """
                    INSERT INTO document_chunks (document_id, chunk_index, chunk_text, token_count, embedding)
                    VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    document_id,
                    i,
                    chunk["chunk_text"],
                    chunk["token_count"],
                    embedding,
                ),
            )

    return document_id
