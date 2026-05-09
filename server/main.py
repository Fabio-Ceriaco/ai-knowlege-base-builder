"""FastAPI application entrypoint. Run with: uvicorn server.main:app --reload"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.middleware.auth import WebhookSecretMiddleware
from server.routers import health, stats, documents, ingest, ask, gaps, analytics

app = FastAPI(
    title="AI Knwledge Base Builder",
    description="RAG-powered knowledge base with pgvector and Voyage embeddings",
    version="0.1.0",
)

# Middleware runs on every request before route matching
app.add_middleware(WebhookSecretMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://vascof.retool.com", "https://retool.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers keep endpoint groups in separate files
app.include_router(health.router)
app.include_router(stats.router)
app.include_router(documents.router)
app.include_router(ingest.router)
app.include_router(ask.router)
app.include_router(gaps.router)
app.include_router(analytics.router)
