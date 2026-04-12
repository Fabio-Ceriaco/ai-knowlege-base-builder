# CLAUDE.md — AI Knowledge Base Builder

# Portfolio Project 2 — Context File for New Chat Session

---

## About Me

- **Name:** Fábio Ceriaco
- **Role:** Technical Support Engineer & AI Automation Specialist
- **Completed:** Anthropic Python SDK curriculum (11 modules)
- **Published:** `anthropic-production-client` production wrapper on GitHub
- **Stack:** Python, JavaScript, Retool (Apps + Workflows), PostgreSQL, REST APIs, Power BI
- **Code style:** Production-grade with defensive caps (MAX_ITERATIONS), try/catch per iteration,
  object parameter passing, spread operator over .concat(), inline comments
- **Learning preference:** Hands-on, step-by-step in chat — never downloadable files unless explicitly a deliverable
- **Available time:** 2-4 hours/week
- **Work and Learn mode** — always explain WHY behind every approach, design decision, and code pattern

---

## Project 1 — Already Complete (for context)

Portfolio Project 1 was an AI-Powered Support Ticket Classifier & Router.

**Stack used:**

- Python + FastAPI webhook server
- PostgreSQL (Supabase) with custom ENUM types
- Anthropic Claude API (claude-sonnet-4-5) for classification
- Retool Workflows (scheduled, every 15 min) + Retool Apps (dashboard)
- ngrok for localhost → Retool Cloud connectivity

**Key patterns established (reuse in Project 2):**

- `.env` file for all secrets, loaded with `set -a && source .env && set +a`
- `DB_CONFIG` dict reads from `os.environ.get()`
- FastAPI with `X-Webhook-Secret` header middleware for auth
- Retry logic with exponential backoff (MAX_RETRIES=3, BACKOFF_BASE=2)
- `stop_reason` guard before parsing Claude responses
- Structured JSON output from Claude — no markdown, no backticks
- Failures table in DB for every API/parse error
- Supabase connection pooler (port 6543) for Retool Cloud IPv4 compatibility
- JS query with Additional scope in Retool to bypass ENUM parameterization issues

**Supabase instance (shared with Project 2):**

- Host: `db.imitaaxfvzidtqhoikhi.supabase.co`
- Pooler: `aws-0-eu-west-1.pooler.supabase.com:6543`
- Database: `postgres`
- User (pooler): `postgres.imitaaxfvzidtqhoikhi`

---

## Project 2 — AI Knowledge Base Builder

### Concept

A system that ingests any document (PDF, markdown, plain text), chunks and embeds it
using the Anthropic Embeddings API, stores vectors in pgvector (PostgreSQL extension),
and answers natural language questions via RAG (Retrieval-Augmented Generation).

It also surfaces **coverage gaps** — topics users asked about that no document covers —
and presents everything in a Retool dashboard.

---

### Architecture

```
[Document Upload]
      │
      ▼
FastAPI /ingest  (multipart/form-data — PDF, .md, .txt)
      │
      ▼
[Text Extraction + Chunking]
  - PDF → PyMuPDF (fitz)
  - Markdown/text → direct read
  - Chunk size: 1024 tokens
  - Overlap: 128 tokens (prevents context loss at chunk boundaries)
      │
      ▼
[Anthropic Embeddings API]
  - Model: voyage-3
  - Input: each chunk text
  - Output: float vector per chunk
      │
      ▼
[pgvector — Supabase]
  - document_chunks table
  - vector(1024) column
  - ivfflat index for ANN search
      │
      ▼
FastAPI /ask  (question → semantic search → RAG → answer)
      │
      ├── Embed question → voyage-3
      ├── Top-5 chunks by cosine similarity
      ├── max_similarity check → gap detection (threshold: 0.80)
      ├── Claude API → answer with source citations
      └── Log to questions_log + coverage_gaps (if gap)
      │
      ▼
[Retool Dashboard]
  - Document library (upload + metadata)
  - Q&A interface (ask question, see answer + sources)
  - Source citation panel (which chunks answered the question)
  - Gap analysis view (unanswered questions clustered by topic)
```

---

### New Technologies vs Project 1

| Technology                           | Purpose                                           | Why chosen                                              |
| ------------------------------------ | ------------------------------------------------- | ------------------------------------------------------- |
| pgvector                             | Vector similarity search inside PostgreSQL        | Keeps everything in one DB — no external vector service |
| Voyage AI Embeddings API(voyage-3.5) | Convert text chunks to vectors                    | Native to Anthropic stack, high quality embeddings      |
| RAG pattern                          | Retrieve relevant chunks before generating answer | Grounds Claude in actual document content               |
| PyMuPDF (fitz)                       | PDF text extraction                               | Fast, accurate, handles multi-page PDFs                 |
| multipart/form-data                  | File upload endpoint                              | Enables direct document upload from Retool or curl      |
| Gap detection                        | Log unanswered questions                          | Surfaces knowledge base weaknesses automatically        |

---

### Key Design Decisions — All Locked

| Decision             | Value                 | Rationale                                                            |
| -------------------- | --------------------- | -------------------------------------------------------------------- |
| Chunk size           | 1024 tokens           | Balance between context richness and retrieval precision             |
| Chunk overlap        | 128 tokens            | Prevents losing context at chunk boundaries                          |
| Top-K retrieval      | 5 chunks              | Enough context without overwhelming Claude's prompt                  |
| Gap threshold        | max_similarity < 0.80 | No chunk scores above 0.80 = knowledge base doesn't cover this topic |
| Embedding model      | voyage-3.5            | Best Anthropic-native embedding model                                |
| Generation model     | claude-sonnet-4-5     | Same as Project 1 — consistent, production-grade                     |
| Vector DB            | pgvector in Supabase  | Same DB instance as Project 1 — no new infrastructure                |
| File types supported | PDF, .md, .txt        | Covers the most common knowledge base document types                 |

---

### Database Schema

#### Enable pgvector extension first:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

#### Tables:

**documents** — document metadata

```
id              SERIAL PRIMARY KEY
title           VARCHAR(300) NOT NULL
source_type     VARCHAR(50)              -- 'pdf', 'markdown', 'text'
file_name       VARCHAR(300)
file_size_bytes INTEGER
chunk_count     INTEGER
ingested_at     TIMESTAMPTZ DEFAULT NOW()
updated_at      TIMESTAMPTZ DEFAULT NOW()
status          VARCHAR(50) DEFAULT 'active'  -- 'active', 'archived'
```

**document_chunks** — text chunks with embeddings

```
id              SERIAL PRIMARY KEY
document_id     INTEGER REFERENCES documents(id)
chunk_index     INTEGER                  -- position within document (0-based)
chunk_text      TEXT NOT NULL
token_count     INTEGER
embedding       vector(1024)             -- voyage-3 produces 1024-dim vectors
created_at      TIMESTAMPTZ DEFAULT NOW()
```

**questions_log** — every question asked + answer + retrieval metadata

```
id              SERIAL PRIMARY KEY
question        TEXT NOT NULL
answer          TEXT
chunk_ids       INTEGER[]                -- IDs of chunks used to answer
max_similarity  NUMERIC(6,4)             -- highest cosine similarity score found
is_gap          BOOLEAN DEFAULT FALSE    -- TRUE if max_similarity < 0.80
asked_at        TIMESTAMPTZ DEFAULT NOW()
model_used      VARCHAR(100)
response_ms     INTEGER                  -- latency in milliseconds
```

**coverage_gaps** — unanswered or low-confidence questions

```
id              SERIAL PRIMARY KEY
question_id     INTEGER REFERENCES questions_log(id)
question        TEXT NOT NULL
max_similarity  NUMERIC(6,4)
gap_topic       TEXT                     -- Claude-inferred topic label
reviewed        BOOLEAN DEFAULT FALSE    -- agent marked as reviewed
created_at      TIMESTAMPTZ DEFAULT NOW()
```

#### Indexes:

```sql
-- ANN vector search index (ivfflat)
CREATE INDEX idx_chunks_embedding
    ON document_chunks
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- Gap queue index
CREATE INDEX idx_gaps_reviewed
    ON coverage_gaps (reviewed)
    WHERE reviewed = FALSE;

-- Document lookup
CREATE INDEX idx_chunks_document_id
    ON document_chunks (document_id);
```

---

### API Endpoints

| Method | Endpoint            | Auth | Description                            |
| ------ | ------------------- | ---- | -------------------------------------- |
| GET    | /health             | No   | Health check                           |
| GET    | /stats              | Yes  | Document count, chunk count, gap count |
| POST   | /ingest             | Yes  | Upload and process a document          |
| POST   | /ask                | Yes  | Ask a question, get RAG answer         |
| GET    | /gaps               | Yes  | List unreviewed coverage gaps          |
| PATCH  | /gaps/{id}/reviewed | Yes  | Mark a gap as reviewed                 |
| GET    | /documents          | Yes  | List all ingested documents            |
| DELETE | /documents/{id}     | Yes  | Remove a document and its chunks       |

---

### FastAPI Server — Key Patterns

```python
# /ingest — multipart file upload
@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    # 1. Read file bytes
    # 2. Extract text (PDF → fitz, .md/.txt → direct decode)
    # 3. Chunk text (1024 tokens, 128 overlap)
    # 4. Embed each chunk (voyage-3 via Anthropic)
    # 5. Write document + chunks to DB
    # 6. Return {document_id, chunk_count, title}

# /ask — RAG query flow
@app.post("/ask")
def ask(payload: AskRequest):
    # 1. Embed question (voyage-3)
    # 2. pgvector cosine similarity search → top 5 chunks
    # 3. Check max_similarity < 0.80 → flag gap
    # 4. Build prompt: system + chunks as context + question
    # 5. Claude API → answer with citations
    # 6. Log to questions_log
    # 7. If gap → write to coverage_gaps
    # 8. Return {answer, sources, max_similarity, is_gap}
```

---

### RAG Prompt Pattern

```python
SYSTEM_PROMPT = """You are a knowledge base assistant.
Answer questions using ONLY the provided document chunks.
Always cite your sources using [Chunk X] notation.
If the chunks do not contain enough information to answer confidently,
say so explicitly — do not hallucinate.
Return a JSON object with these keys:
{
    "answer": "<your answer with [Chunk N] citations>",
    "confidence": <float 0.0-1.0>,
    "cited_chunks": [<list of chunk indices used>],
    "is_answerable": <true|false>
}"""
```

---

### Retool Dashboard — 4 Views

**View 1 — Document Library**

- Table: all documents (title, type, chunk_count, ingested_at, status)
- Upload button → POST /ingest via fetch() JS query
- Delete button → DELETE /documents/{id}
- Stats: total docs, total chunks

**View 2 — Q&A Interface**

- Text input: question
- Submit button → POST /ask
- Answer panel: rendered answer text
- Source citations panel: chunk_text for each cited chunk
- Confidence badge + gap warning if is_gap = true

**View 3 — Gap Analysis**

- Table: coverage_gaps WHERE reviewed = FALSE
- Columns: question, max_similarity, gap_topic, created_at
- Mark reviewed button → PATCH /gaps/{id}/reviewed
- Stats: total gaps, gaps this week

**View 4 — Analytics**

- Questions per day (line chart)
- Top gap topics (bar chart)
- Average similarity score trend
- Most queried documents

---

### Project Folder Structure

```
project_2_knowledge_base/
│
├── .env                          # Environment variables — never commit
├── .gitignore                    # Excludes .env, venv/, __pycache__, uploads/
├── README.md                     # Project overview
├── CLAUDE.md                     # This file — context for Claude
├── requirements.txt              # Python dependencies
│
├── server/
│   ├── __init__.py
│   ├── main.py                   # FastAPI app — registers all routers
│   ├── config.py                 # DB_CONFIG, env vars, constants
│   ├── database.py               # psycopg2 connection helpers
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── ingest.py             # POST /ingest
│   │   ├── ask.py                # POST /ask
│   │   ├── gaps.py               # GET /gaps, PATCH /gaps/{id}/reviewed
│   │   ├── documents.py          # GET /documents, DELETE /documents/{id}
│   │   └── health.py             # GET /health, GET /stats
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── extractor.py          # PDF + text extraction
│   │   ├── chunker.py            # 1024-token chunking with 128 overlap
│   │   ├── embedder.py           # Anthropic voyage-3 embeddings
│   │   ├── retriever.py          # pgvector cosine similarity search
│   │   └── generator.py          # Claude RAG answer generation
│   │
│   └── middleware/
│       ├── __init__.py
│       └── auth.py               # X-Webhook-Secret header validation
│
├── scripts/
│   ├── setup_db.sql              # pgvector + ENUMs + tables + indexes
│   ├── seed_documents.py         # Ingest sample documents for testing
│   └── test_ask.py               # CLI test — python test_ask.py "your question"
│
└── uploads/                      # Temp storage for uploaded files (gitignored)
```

---

### Environment Variables (.env)

```bash
ANTHROPIC_API_KEY="sk-ant-..."
WEBHOOK_SECRET="your-webhook-secret-here"
DB_HOST="aws-0-eu-west-1.pooler.supabase.com"
DB_PORT="6543"
DB_NAME="postgres"
DB_USER="postgres.imitaaxfvzidtqhoikhi"
DB_PASSWORD="your-supabase-password"
EMBEDDING_MODEL="voyage-3"
GENERATION_MODEL="claude-sonnet-4-5"
TOP_K="5"
GAP_THRESHOLD="0.80"
CHUNK_SIZE="1024"
CHUNK_OVERLAP="128"
```

---

### Python Dependencies (requirements.txt)

```
anthropic
fastapi
uvicorn
psycopg2-binary
pydantic
python-multipart       # required for FastAPI file uploads
pymupdf                # PDF extraction (import as fitz)
tiktoken               # token counting for chunking
numpy                  # vector operations
```

---

### 4-Week Build Plan

| Week   | Deliverables                                                                                                                       |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| Week 1 | pgvector setup in Supabase, full DB schema (4 tables + indexes), extractor + chunker + embedder services, seed_documents.py script |
| Week 2 | FastAPI server with all 8 endpoints, RAG query flow (/ask), gap detection logic, questions_log + coverage_gaps writes              |
| Week 3 | Retool Dashboard — Document Library, Q&A Interface, Source Citation Panel, Gap Analysis View                                       |
| Week 4 | Analytics view, chunk overlap tuning, gap topic clustering via Claude, README + Word doc                                           |

---

### Rules for This Project

- Always use production-grade patterns (error handling, defensive coding, inline comments)
- All Claude API calls follow Module 11 wrapper patterns (retry, backoff, stop_reason guard)
- Structured JSON output from Claude — no markdown in API responses
- Modular server structure — one router per endpoint group, one service per concern
- Deliver everything step-by-step in chat, not as file downloads
- Never hallucinate numbers, data, code structures, or API signatures
- Always validate embedding dimensions before INSERT (voyage-3 = 1024 dims)
- Always check pgvector index exists before running similarity queries

---

### How to Start Project 2 in a New Chat

1. Create a new Claude Project (or new chat in existing project)
2. Upload this CLAUDE.md as project context
3. Start with:

> "I am starting Portfolio Project 2 — AI Knowledge Base Builder.
> All context is in CLAUDE.md. I am ready for Week 1, Step 1."

Claude will pick up exactly where this file leaves off.

---

### Where Week 1 Starts

**Step 1 — Enable pgvector in Supabase SQL Editor:**

```sql
CREATE EXTENSION IF NOT EXISTS vector;
SELECT * FROM pg_extension WHERE extname = 'vector';
```

**Step 2 — Run setup_db.sql** (Claude will provide this) — creates all 4 tables + indexes.

**Step 3 — Build extractor.py** — PDF + markdown + text extraction service.

**Step 4 — Build chunker.py** — 1024-token chunking with 128-token overlap using tiktoken.

**Step 5 — Build embedder.py** — voyage-3 embeddings via Anthropic API.

**Step 6 — seed_documents.py** — ingest 5 sample documents across different types.

```

```
