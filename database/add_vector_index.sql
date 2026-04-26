-- IVFFlat index for approximate nearest-neighbour search on embeddings.
-- Speeds up cosine distance queries (<=> operator) from O(n) full-scan
-- to O(sqrt(n)) once the table grows beyond a few thousand chunks.
--
-- lists=100 is the standard starting point for up to ~1M rows.
-- Re-run ANALYZE after adding significant new data so the planner uses it.

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_document_chunks_embedding
    ON document_chunks
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

ANALYZE document_chunks;
