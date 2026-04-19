-- ============================================================
-- Step 1: Enable pgvector extension
-- ============================================================
-- WHY: Adds the 'vector' data type and similarity operators
-- (cosine distance, inner product, L2 distance) to PostgreSQL.
-- Without this, we cannot store or search embeddings.
-- IF NOT EXISTS = idempotent — safe to run multiple times.
-- ============================================================

create extension if not exists vector;

-- Verify installation - expect one row with extname = 'vector'

select extname, extversion
from pg_extension
where extname = 'vector';


-- ============================================================
-- setup_db.sql — AI Knowledge Base Builder
-- Project 2 — Full schema: 4 tables + 3 indexes
-- ============================================================
-- PREREQUISITE: pgvector extension must be enabled first
--   CREATE EXTENSION IF NOT EXISTS vector;
-- ============================================================

-- ============================================================
-- TABLE 1: documents
-- Purpose: Parent record for each uploaded file (PDF, .md, .txt)
-- One row per document. Chunks reference this via document_id.
-- ============================================================


create table if not  exists documents(
	id 				serial primary key,
	title 			varchar(300) not null,			-- document title (extracted or user-provided)
	source_type		varchar(50),					-- 'pdf', 'markdown', 'text'
	file_name		varchar(300),					-- original upload filename
	file_size_bytes	integer,						-- file size for metadata tracking
	chunk_count		integer,						-- total chunks produced from this document
	ingested_at		timestamptz default now(),		-- when the document was processed
	updated_at		timestamptz default now(),		-- last modification timestamp
	status			varchar(50) default 'active'	-- 'active' or 'archived'
);


-- ============================================================
-- TABLE 2: document_chunks
-- Purpose: Individual text chunks with their vector embeddings.
-- This is the table pgvector searches during /ask queries.
-- Each chunk belongs to exactly one document (document_id FK).
-- ============================================================

create table if not exists document_chunks (
	id 						serial primary key,
	document_id				integer references documents(id) on delete cascade,
	chunk_index				integer,			-- position within document (0-based)
	chunk_text				text not null ,		-- the actual text content
	token_count				integer,			-- token count for prompt budget
	embedding				vector(1024),		-- voyage-3 produces 1024-dimensional vectors
	created_at				timestamptz	default now()
);


-- ============================================================
-- TABLE 3: questions_log
-- Purpose: Audit trail — every question asked, the answer given,
-- which chunks were used, similarity scores, and latency.
-- Used for analytics, debugging, and gap detection.
-- ============================================================


create table if not exists questions_log (
	id						serial primary key,
	question 				text not null,
	answer					text,
	chunks_ids				integer[],				-- array of chunks ID's used to generate answer
	max_similarity			numeric(6,4),			-- highest consise similarity score found
	is_gap					boolean default false,	-- true if max_similarity < 0.80 threshold
	asked_at				timestamptz default now(),
	model_used				varchar(100),			-- e.g. 'claude-sonnet-4-6'
	response_ms				integer					-- end-to-end latency in milliseconds
);

-- ============================================================
-- TABLE 4: coverage_gaps
-- Purpose: Work queue for knowledge base gaps.
-- A gap = a question where no chunk scored above the 0.80 threshold.
-- Human reviews each gap and decides whether to add new documents.
-- ============================================================

create table if not exists coverage_gaps(
	id						serial primary key,
	question_id				integer references questions_log(id) on delete cascade,
	question				text not null,				-- duplicated for quick access without JOIN
	max_similarity          numeric(6,4),
	gap_topic				text,						-- Claude-inferred topic label for clustering
	reviewed				boolean default false, 		-- true after human marks it as reviewed 
	created_at				timestamptz default now()
);


-- ============================================================
-- INDEX 1: Document lookup on chunks
-- WHY: Speeds up DELETE cascades and document-scoped queries.
-- ============================================================

create index if not exists idx_chunks_document_id
	on document_chunks (document_id);


-- ============================================================
-- INDEX 2: Gap work queue — partial index
-- WHY: Only indexes unreviewed gaps. Dashboard query
--   "SELECT * FROM coverage_gaps WHERE reviewed = FALSE"
--   hits this index directly, skipping all reviewed rows.
-- ============================================================


create index if not exists idx_gaps_reviewed
	on coverage_gaps (reviewed)
	where reviewed = false;



-- ============================================================
-- INDEX 3: Vector similarity search (ivfflat) — DEFERRED
-- WHY: ivfflat requires existing data to build clusters.
-- DO NOT run this until AFTER seeding data in Step 6.
-- Uncomment and run after seed_documents.py has inserted chunks.
-- ============================================================

create index if not exists idx_chunks_embedding
		on document_chunks
		using ivfflat (embedding vector_cosine_ops)
		with (lists = 100);



-- ============================================================
-- VERIFY: Check all tables were created
-- ============================================================

select table_name
from information_schema."tables" t 
where t.table_schema = 'public'
	and t.table_name in ('documents', 'document_chunks', 'questions_log', 'coverage_gaps')
order by t.table_name;


-- ============================================================
-- Verify constraint name
-- ============================================================

SELECT conname, pg_get_constraintdef(oid) AS definition
FROM pg_constraint
WHERE conrelid = 'document_chunks'::regclass
  AND contype = 'f';



-- ============================================================
-- ALTER
-- ============================================================

BEGIN;

ALTER TABLE document_chunks
    DROP CONSTRAINT document_chunks_document_id_fkey;

ALTER TABLE document_chunks
    ADD CONSTRAINT document_chunks_document_id_fkey
    FOREIGN KEY (document_id)
    REFERENCES documents(id)
    ON DELETE CASCADE;

COMMIT;









































