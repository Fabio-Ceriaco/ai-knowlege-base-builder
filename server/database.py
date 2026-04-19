"""
Databease connection layer for the AI Knowledge Base Builder.

Provides context-managed psycopg2 connections with the pgvector adapter
pre-registered, so any caller can INSERT/SELECT vestor(1024) columns
using plain Python lists or numpy arrays without manual serialization.
"""

import psycopg2
from contextlib import contextmanager
from psycopg2.extras import RealDictCursor
from pgvector.psycopg2 import register_vector
from server.utils.config import settings


# DB config

DB_CONFIG = {
    "host": settings.DB_HOST,
    "port": settings.DB_PORT,
    "dbname": settings.DB_NAME,
    "user": settings.DB_USER,
    "password": settings.DB_PASSWORD,
}


@contextmanager
def get_connection():
    """
    Yields a psycopg2 connection with the pgvector adapter registered.

    The context manager guarantees .close() runs even if the caller
    raises mid-transaction. replaces the manual try/finally boilerplate.

    Usage:
        with get_connection() as conn:
            witt conn.cursor() as cur:
                cur.execute("SELECT 1")
    """
    conn = psycopg2.connect(**DB_CONFIG)

    try:
        # Teach psycopg2 how to (de)serialize vector(n) columns.
        # Must run on every fresh connection - it's per-connection state, not global.
        register_vector(conn)
        yield conn
    finally:
        conn.close()


@contextmanager
def get_cursor(commit: bool = True):
    """
    Yields a RealDictCursor inside a managed connection.

    RealDictCursor: rows come back as dicts (row["title"]) insted of
    tuples (row[0]). Eliminates "wrong column index" bugs and makes the
    rows JSON-serializable for FastAPI responses with zero mapping code.

    The commit flag: read-only callers (SELECT only) pass commit=False
    to skip the commit roundtrip. Write callers leave it True, and on any
    exception we rollback automatically before propagating.
    """
    with get_connection() as conn:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            yield cur
            if commit:
                conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()
