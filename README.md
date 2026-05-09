# AI Knowledge Base Builder

**Portfolio Project 2 — Fábio Ceriaco**
Technical Support Engineer & AI Automation Specialist

A system that ingests technical documents, chunks and embeds them using Voyage AI, stores vectors in PostgreSQL via pgvector, and answers natural language questions using Retrieval-Augmented Generation (RAG) with Claude.

It also automatically detects **coverage gaps** — topics users asked about that no document covers — and labels them using Claude for analysis.

---

## What It Does

- **Document ingestion** — upload PDF, Markdown, or plain text files via REST API
- **Semantic search** — questions are embedded and matched against document chunks using cosine similarity
- **RAG answers** — Claude answers using only retrieved chunks, with source citations
- **Gap detection** — questions that score below the similarity threshold are flagged and logged
- **Gap topic clustering** — each gap is automatically labelled by Claude (e.g. "Kubernetes Basics")
- **Retool dashboard** — four views: Document Library, Q&A Interface, Gap Analysis, Analytics

---

## Tech Stack

| Layer | Technology |
|---|---|
| API server | FastAPI + uvicorn |
| Embeddings | Voyage AI (`voyage-3.5`, 1024-dim) |
| Vector search | pgvector (PostgreSQL extension) |
| Generation | Anthropic Claude (`claude-sonnet-4-6`) |
| Database | PostgreSQL via Supabase |
| Dashboard | Retool Cloud |
| Tunnel | ngrok (static domain) |

---

## Project Structure

```
project_2_knowledge_base/
│
├── .env                          # Environment variables — never commit
├── .gitignore
├── README.md
├── CLAUDE.md                     # Project context file
├── requirements.txt
│
├── server/
│   ├── main.py                   # FastAPI app — router registration + middleware
│   ├── config.py                 # Settings from environment variables
│   ├── database.py               # psycopg2 connection + cursor helpers
│   │
│   ├── routers/
│   │   ├── health.py             # GET /health, GET /stats
│   │   ├── ingest.py             # POST /ingest
│   │   ├── ask.py                # POST /ask
│   │   ├── gaps.py               # GET /gaps, PATCH /gaps/{id}/reviewed
│   │   ├── documents.py          # GET /documents, DELETE /documents/{id}
│   │   └── analytics.py          # GET /analytics/*
│   │
│   ├── services/
│   │   ├── extractor.py          # PDF + markdown + text extraction
│   │   ├── chunker.py            # Token-based chunking (tiktoken)
│   │   ├── embedder.py           # Voyage AI embeddings
│   │   ├── retriever.py          # pgvector cosine similarity search
│   │   └── generator.py          # Claude RAG generation + gap topic labelling
│   │
│   └── middleware/
│       └── auth.py               # X-Webhook-Secret header validation
│
├── scripts/
│   ├── setup_db.sql              # pgvector + tables + indexes
│   ├── seed_documents.py         # Ingest sample documents
│   └── test_ask.py               # CLI question tester
│
└── uploads/                      # Temporary file storage (gitignored)
```

---

## Prerequisites

- Python 3.11+
- macOS
- A [Supabase](https://supabase.com) project with pgvector enabled
- An [Anthropic](https://console.anthropic.com) API key (covers Voyage AI and Claude)
- A [Retool Cloud](https://retool.com) account
- [ngrok](https://ngrok.com) with a static domain

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/project_2_knowledge_base.git
cd project_2_knowledge_base
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your values:

```bash
ANTHROPIC_API_KEY="sk-ant-..."
WEBHOOK_SECRET="your-webhook-secret"
DB_HOST="aws-0-eu-west-1.pooler.supabase.com"
DB_PORT="6543"
DB_NAME="postgres"
DB_USER="postgres.your-project-id"
DB_PASSWORD="your-supabase-password"
EMBEDDING_MODEL="voyage-3.5"
GENERATION_MODEL="claude-sonnet-4-6"
TOP_K="5"
GAP_THRESHOLD="0.70"
CHUNK_SIZE="1024"
CHUNK_OVERLAP="128"
```

### 5. Set up the database

In your Supabase SQL editor, enable pgvector:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Then run the schema by pasting `scripts/setup_db.sql` into the Supabase SQL editor.

### 6. Load environment and start the server

```bash
set -a && source .env && set +a
uvicorn server.main:app --reload --port 8000
```

### 7. Start ngrok tunnel

```bash
ngrok http --domain=your-static-domain.ngrok-free.app 8000
```

---

## Seed Documents

The project was developed with 5 Markdown documents as the knowledge base:

| Document | File | Size |
|---|---|---|
| Anthropic documentation | `anthropic.md` | 22 KB |
| PostgreSQL documentation | `postgresql.md` | 36 KB |
| Retool documentation | `retool.md` | 37 KB |
| JavaScript tutorial | `javascript.md` | 21 KB |
| FastAPI documentation | `fastapi.md` | 25 KB |

To ingest your own documents:

```bash
curl -X POST https://your-domain.ngrok-free.app/ingest \
  -H "X-Webhook-Secret: your-secret" \
  -F "file=@your-document.md"
```

---

## API Endpoints

All authenticated endpoints require the header: `X-Webhook-Secret: your-secret`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/health` | No | Health check |
| GET | `/stats` | Yes | Aggregate counts |
| GET | `/documents` | Yes | List all documents |
| DELETE | `/documents/{id}` | Yes | Delete document and its chunks |
| POST | `/ingest` | Yes | Upload and process a document |
| POST | `/ask` | Yes | Ask a question, get RAG answer |
| GET | `/gaps` | Yes | List unreviewed coverage gaps |
| PATCH | `/gaps/{id}/reviewed` | Yes | Mark a gap as reviewed |
| GET | `/analytics/questions-per-day` | Yes | Question volume by day (last 30 days) |
| GET | `/analytics/gap-topics` | Yes | Open gaps grouped by topic |
| GET | `/analytics/similarity-trend` | Yes | Average similarity score by day |
| GET | `/analytics/top-documents` | Yes | Most queried documents by chunk usage |

### Example — Ask a question

```bash
curl -X POST https://your-domain.ngrok-free.app/ask \
  -H "X-Webhook-Secret: your-secret" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is FastAPI?"}'
```

Response:

```json
{
  "answer": "FastAPI is a modern, high-performance web framework... [Chunk 0]",
  "confidence": 0.9,
  "is_answerable": true,
  "cited_chunks": [0, 1],
  "max_similarity": 0.7876,
  "is_gap": false,
  "question_id": 24,
  "model_used": "claude-sonnet-4-6",
  "response_ms": 4717
}
```

---

## How RAG Works in This Project

```
User question
      │
      ▼
Embed question (Voyage AI voyage-3.5)
      │
      ▼
pgvector cosine similarity search → top 5 chunks
      │
      ├── max_similarity < 0.70 → gap detected
      │         │
      │         ▼
      │   Write to coverage_gaps
      │   Claude labels gap_topic inline
      │
      ▼
Build prompt: system + chunks + question
      │
      ▼
Claude (claude-sonnet-4-6) → structured JSON answer
      │
      ▼
Log to questions_log → return answer + sources + metadata
```

**Gap threshold:** 0.70. Calibrated empirically against voyage-3.5's cosine similarity distribution — covered topics score 0.71–0.79, uncovered topics score below 0.65.

**Chunking:** 1024-token chunks with 128-token overlap using tiktoken (`cl100k_base`). Overlap prevents context loss at chunk boundaries.

**Embeddings:** Asymmetric — documents ingested with `input_type="document"`, queries embedded with `input_type="query"`. This matches Voyage AI's intended usage for retrieval tasks.

---

## Retool Dashboard

Four views connected to the FastAPI server via REST resource over ngrok:

| View | Description |
|---|---|
| **Documents** | Upload documents, view metadata, delete |
| **Questions** | Ask questions, see answers with source citations and confidence score |
| **Gaps** | Review unanswered questions grouped by topic, mark as reviewed |
| **Analytics** | Questions per day, similarity trend, top gap topics, most queried documents |

---

## Key Design Decisions

**Why pgvector instead of a dedicated vector database?**
Keeps the entire system in one PostgreSQL instance — the same Supabase project used in Portfolio Project 1. No additional infrastructure, no new connection management.

**Why Voyage AI for embeddings?**
Voyage AI is Anthropic's recommended embedding provider and produces 1024-dimensional vectors optimised for retrieval tasks. The asymmetric `input_type` parameter (`document` vs `query`) meaningfully improves retrieval quality over symmetric embeddings.

**Why a gap threshold of 0.70?**
Empirically calibrated. voyage-3.5 cosine similarity scores for covered topics peak at ~0.79. Scores for genuinely uncovered topics sit at ~0.61–0.65. The 0.70 boundary cleanly separates the two distributions with no false positives in testing.

**Why label gap topics inline rather than in a background worker?**
Insert-then-label within the same `/ask` request keeps the system simple and ensures every gap has a topic immediately. The labelling Claude call adds ~200ms to gap responses — acceptable given that gaps are already slower paths (low similarity means less certain retrieval).

---

## Environment Variables Reference

| Variable | Description | Example |
|---|---|---|
| `ANTHROPIC_API_KEY` | Anthropic API key | `sk-ant-...` |
| `WEBHOOK_SECRET` | Auth header value | `my-secret` |
| `DB_HOST` | Supabase pooler host | `aws-0-eu-west-1.pooler.supabase.com` |
| `DB_PORT` | Supabase pooler port | `6543` |
| `DB_NAME` | Database name | `postgres` |
| `DB_USER` | Pooler user | `postgres.project-id` |
| `DB_PASSWORD` | Database password | — |
| `EMBEDDING_MODEL` | Voyage AI model | `voyage-3.5` |
| `GENERATION_MODEL` | Claude model | `claude-sonnet-4-6` |
| `TOP_K` | Chunks retrieved per query | `5` |
| `GAP_THRESHOLD` | Similarity threshold for gap detection | `0.70` |
| `CHUNK_SIZE` | Tokens per chunk | `1024` |
| `CHUNK_OVERLAP` | Overlap tokens between chunks | `128` |

---

## Author

**Fábio Ceriaco**
Technical Support Engineer & AI Automation Specialist
[GitHub](https://github.com/your-username)
