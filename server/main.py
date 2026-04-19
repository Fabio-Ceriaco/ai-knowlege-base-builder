"""FastAPI application entrypoint. Run with: uvicorn server.main:app --reload"""

from fastapi import FastAPI

from server.middleware.auth import WebhookSecretMiddleware
from server.routers import health, stats, documents, ingest

app = FastAPI(
    title="AI Knwledge Base Builder",
    discription="RAG-powered knowledge base with pgvector and Voyage embeddings",
    version="0.1.0",
)

# Middleware runs on every request before route matching
app.add_middleware(WebhookSecretMiddleware)

# Routers keep endpoint groups in separate files
app.include_router(health.router)
app.include_router(stats.router)
app.include_router(documents.router)
app.include_router(ingest.router)
