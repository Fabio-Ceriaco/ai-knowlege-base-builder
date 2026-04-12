"""
Standalone test for database layer.

Inserts a fake document +3 fake chunks with dummy 1024-dim vectors,
runs a consine-similarity query against them, then cleans up.
"""

import sys
from pathlib import Path


sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent)
)  # this allows us to import from the parent directory

from server.database import get_cursor

# Dummy 1024-dim vector. Real embedding from voyage-3,4 will be unit-norm
# floats in roughly [-0.1, 0.1]; 0.1 acorss all dims is fine for a smoke test.get_cursor

DUMMY_VECTOR = [0.1] * 1024


def main():
    # 1. Insert one document, capture its ID
    with get_cursor() as cur:
        cur.execute(
            """
                INSERT INTO documents (title, source_type, file_name, file_size_bytes, chunk_count)
                VALUES (%s,%s,%s,%s,%s)
                RETURNING id
            """,
            ("TEST_DOC_DELETE_ME", "text", "test.txt", 123, 3),
        )

        document_id = cur.fetchone()["id"]
        print(f"[1/4] Inserted document id = {document_id}")

    # 2. Insert 3 chunks tied to that document
    # DUMMY_VECTOR is pass as plain Python list. Because register_vector()
    # ran on this connection, psycopg2 serializes it to pgvector format automatically.
    # Without the adapter this have to be done manually.def

    with get_cursor() as cur:
        for i in range(3):
            cur.execute(
                """
                    INSERT INTO document_chunks (document_id, chunk_index, chunk_text, token_count, embedding)
                    VALUES (%s, %s, %s, %s, %s)
                """,
                (document_id, i, f"This is dummy chunk {i}", 5, DUMMY_VECTOR),
            )
        print(f"[2/4] Inserted 3 chunks")

    # 3. Read back with a join, prove round-trip works

    with get_cursor() as cur:
        cur.execute(
            """
                SELECT 
                    d.title,
                    c.chunk_index,
                    c.chunk_text
                FROM documents d
                JOIN document_chunks c 
                    ON c.document_id = d.id
                WHERE d.id = %s
                ORDER BY c.chunk_index
            """,
            (document_id,),
        )

        rows = cur.fetchall()
        assert (
            len(rows) == 3
        ), f"Expected 3 chunks, got {len(rows)}"  # assert is used to check if a condition is true, if not it will raise an error
        print(f"[3/4] Read back {len(rows)} chunks: {[r['chunk_text'] for r in rows]}")
    # 4. The important one : cosine similarity query
    # The <=> operator is pgvector's "cosine distance"
    # Distance = 1 - similarity, so identical vectors give distance 0

    with get_cursor() as cur:
        cur.execute(
            """
                SELECT 
                    chunk_index,
                    chunk_text,
                    embedding <=> %s::vector AS distance
                FROM document_chunks
                WHERE document_id = %s
                ORDER BY distance ASC
                LIMIT 5
            """,
            (DUMMY_VECTOR, document_id),
        )

        results = cur.fetchall()
        # Identical vectors -> distance -0.0 (floating point tolerance).
        top_distance = float(results[0]["distance"])
        assert top_distance < 0.001, f"Expected diastance -0, got {top_distance}"
        print(f"[4/4] Cosine query OK - top distance = {top_distance:.6f}")

    # Cleanup : delete the test document

    with get_cursor() as cur:
        cur.execute("DELETE FROM documents WHERE id = %s", (document_id,))
        print(f"[Cleanup] Removed test document id={document_id}")

    print("\nOK - database layer is ready.")


if __name__ == "__main__":
    main()
