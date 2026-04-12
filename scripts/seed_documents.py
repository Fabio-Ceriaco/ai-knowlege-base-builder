"""
Ingets the 5 seed documents from seed_data/ into the knowledge base.

Idempotent: re-running skips documents whose file_name already exists.
After all inserts succeed, builds the invfflat index on documents_chunks.embedding
so /ask endpoint has a tarined index to use.
"""

import sys
import time
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent)
)  # allows us to import from the parent directory

from psycopg2.extras import execute_values

from server.database import get_cursor
from server.services.extractor import extract_text
from server.services.chunker import chunk_text
from server.services.embedder import embed_texts

# seed_data/ lives at project root, same level as scripts/ and server/
SEED_DIR = Path(__file__).resolve().parent.parent / "seed_data"

# Map file extension -> source_type value stored in documents.source_type
# Keeps the column values consistent with what POST /ingest will write later

SOURCE_TYPE_BY_SUFFIX = {
    ".pdf": "pdf",
    ".md": "markdown",
    ".txt": "text",
}


def document_exists(file_name: str) -> int | None:
    """Return the existing document.id for this file_name or None if not ingested yet."""
    # commit=False - this is an read only
    with get_cursor(commit=False) as cur:
        cur.execute("SELECT id FROM documents WHERE file_name = %s", (file_name,))
        row = cur.fetchone()
        return row["id"] if row else None


def ingest_file(path: Path) -> tuple[int, int]:
    """
    Full pipeline for one file: extract -> chunk -> embed -> insert.

    Returns (document_id, chunk_count). Raises on any failure so the caller
    can skip to the next without corrupting the current one's transaction.
    """

    # Extract
    file_bytes = path.read_bytes()
    file_name = path.name
    file_size = len(file_bytes)
    extracted = extract_text(file_bytes, file_name)
    text = extracted["text"]
    source_type = extracted["source_type"]

    # Chunk
    # Returns list of dicts: [{"chunk_index": 0, "text": "...", "token_count": 1024}, ...]
    # Id chunker returns a different shape, adjust the unpacking.
    chunks = chunk_text(text)
    if not chunks:
        raise ValueError(f"Chunker returns 0 chunks for {file_name}")

    # Embed
    # Batch all chunks in one API call. Voyage returns vectors in the same
    # order as inputs, zip() aligns chunk[i] with embedding[i].
    chunks_texts = [c["chunk_text"] for c in chunks]
    embeddings = embed_texts(chunks_texts, input_type="document")
    if len(embeddings) != len(chunks):
        raise ValueError(
            f"Emdedding count mismatch for {file_name}: "
            f"{len(embeddings)} emdeddings for {len(chunks)} chunks."
        )

    # Defensive dimension check, voyage-3.5 = 1024 dims. Catching this here
    # beats a cryptic pgvector error at INSERT time.
    if len(embeddings[0]) != 1024:
        raise ValueError(f"Expected 1024-dim embeddings, got {len(embeddings[0])}")

    # Insert - one transaction, parent then children
    with get_cursor() as cur:
        cur.execute(
            """
                INSERT INTO documents (title, source_type, file_name, file_size_bytes, chunk_count)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """,
            (path.stem, source_type, file_name, file_size, len(chunks)),
        )
        document_id = cur.fetchone()["id"]

        # execute_values batches all chunks into a single INSERT with a
        # multi-row VALUES clause. Much faster than a python loop of execute().
        rows = [
            (document_id, c["chunk_index"], c["chunk_text"], c["token_count"], emb)
            for c, emb in zip(chunks, embeddings)
        ]
        execute_values(
            cur,
            """
                INSERT INTO document_chunks (
                document_id, chunk_index, chunk_text, token_count, embedding)
                VALUES %s
            """,
            rows,
        )

    return document_id, len(chunks)


def build_ivfflat_index() -> None:
    """
    Build the ivfflat index after seeding so it trains on real vectors.

    Note on `lists = 100`: pgvector recommends lists = ~rows/1000. At seed
    scale (~50-200 vectors) this id oversized and the planner may prefer
    sequencial scan.

    `ANALYZE`refreshes planner stats so it knows the new index exists
    and can estimate its slectivity correctly.
    """

    with get_cursor() as cur:
        # IF NOT EXISTS makes this re-runnable alongside the idempotent ingest.
        cur.execute(
            """
                CREATE INDEX IF NOT EXISTS idx_chunks_embedding
                    ON document_chunks
                    USING ivfflat (embedding vector_cosine_ops)
                    WITH (lists = 10);
            """
        )
        cur.execute("ANALYZE document_chunks")


def main():
    if not SEED_DIR.is_dir():
        raise FileNotFoundError(f"Seed directory not found: {SEED_DIR}")

    files = sorted(
        p
        for p in SEED_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in SOURCE_TYPE_BY_SUFFIX
    )

    if not files:
        raise FileNotFoundError(f"No .pdf/.md/.txt files found in {SEED_DIR}")

    print(f"Found {len(files)} candidate file(s) in {SEED_DIR}")

    ingested = skipped = failed = 0
    total_chunks = 0

    for path in files:
        existing_id = document_exists(path.name)
        if existing_id is not None:
            print(f" [skip] {path.name} - already ingested (id={existing_id})")
            skipped += 1
            continue
        t0 = time.perf_counter()
        try:
            doc_id, chunk_count = ingest_file(path)
            elapsed = time.perf_counter() - t0
            print(
                f" [ingest] {path.name} - id={doc_id}, "
                f"chunks={chunk_count}, {elapsed:.2f}s"
            )
            ingested += 1
            total_chunks += chunk_count
        except Exception as e:
            # Pre-document isolation: one bad file doesn't kill the run.
            # The transaction inside ingest_file() already rolled back,
            # so no partial document/chunks remain in the DB.
            print(f" [FAIL] {path.name} - {type(e).__name__}: {e}")
            failed += 1

    print(
        f"\nSummary: {ingested} ingested, {skipped} skipped, {failed} failed, "
        f"{total_chunks} new chunks."
    )

    # Only rebuild the index if we actually added vectors. ivfflat training
    # on unchanged data is wasted work.
    if ingested > 0:
        print("\nBuilding ivfflat index on document_chunks.embedding...")
        build_ivfflat_index()
        print("Index ready.")
    else:
        print("\nNo new vectors - skipping index build.")


if __name__ == "__main__":
    main()
