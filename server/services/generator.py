"""Claude RAG answer generation with structured JSON output."""

import json
import os
import time
import logging
from dotenv import load_dotenv
import anthropic
from server.utils.config import settings

load_dotenv()

logger = logging.getLogger(__name__)

# --- Contigurantion from enviorment ---

GENERATION_MODEL = settings.GENERATION_MODEL

# -- Retry configurantion ---
MAX_RETRIES = 3
BACKOFF_BASE = 2

# --- System prompt ---

SYSTEM_PROMPT = """
    You are a knowledge base assistant.
    Answer questions using ONLY the provided document chunks.
    Always cite your sources using [Chunk N] notation.
    If the chunks do not contain enough information to answer confidently,
    say so explicitly - do not hallucinate.

    Return ONLY a valid JSON object whit this keys (no markdown, no backticks):
    {
        "answer": "<your answer with [Chunk N] citations>",
        "confidence": <float 0.0-1.0>,
        "cited_chunks": [<list of chunks indices used>],
        "is_answerable": <true|false>
    }
"""

# -- Initialize the Anthropic client ---

client = anthropic.Anthropic()


def _format_chunks(chunks: list) -> str:
    """
    Format retrived chgunks into a labeled context block for Claude's prompt.

    Each chunk gets a label like [Chunk 0 - from "fastapi"] so Cluade can:
    1. Cite by chunk index in its answer
    2. See which document each chunk came from

    Why include the document title? Whitout it, Claude cites [Chunk 3] but
    the user has no easy way to know which document [Chunk 3] belongs to.
    Including the title lets the answer say "According to the FastAPI documentation [Chunk 3]..."
    """

    formatted = []
    for chunk in chunks:
        label = f'[Chunk {chunk["chunk_index"]} - from "{chunk["document_title"]}"]'
        formatted.append(f"{label}\n{chunk['chunk_text']}\n")
    return "\n---\n".join(formatted)


def generate_answer(question: str, chunks: list) -> dict:
    """
    Send retrived chunks + question to Claude, get a structured answer.

    Args:
        question: The user's natural language question
        chunks: List of chunk dicts from retriver (must have
                chunk_index, chunk_text, document_title)


    Returns:
        dict with keys:
            - answer (str): Claude's answer with [Chunk N] citations
            - confidence (float): 0.0-1.0
            - cited_chunks (list[int]): chunk indices used
            - is_answerable (bool): whether the chunks covered the question
            - model_used (str): which Claude model was used
            - response_ms (int): latencty in milliseconds

    Raises:
        RuntimeError: Aterf MAX_RETRIES failed attempts
        ValueError: If Claude's response isn't valid JSON
    """

    # --- Build user prompt with chunks as context ---
    context_block = _format_chunks(chunks)
    user_prompt = f"""
        Here are the relevant document chunks:
        {context_block}

        Question: {question}

        Respond with JSON object only.
    """

    # --- Retry loop with exponential backoff ---
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Claude API call - attempt {attempt}/{MAX_RETRIES}")
            start_ms = time.time()

            response = client.messages.create(
                model=GENERATION_MODEL,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt,
                    }
                ],
            )

            elapsed_ms = int((time.time() - start_ms) * 1000)

            # --- stop_reason guard - if response was truncated, JSON is likely broken ---

            if response.stop_reason != "end_turn":
                raise ValueError(
                    f"Unexpexted stop_reason: '{response.stop_reason}'."
                    f"Response may be truncated."
                )

            # Extract text content
            raw_text = response.content[0].text.strip()

            # Strip markdown fences if Claude adds them despite instructions
            clean_text = raw_text
            if clean_text.startswith("```"):
                clean_text = clean_text.lstrip("`")
                if clean_text.startswith("json"):
                    clean_text = clean_text[4:]
                clean_text = clean_text.rstrip("`").strip()

            parsed = json.loads(clean_text)

            # Validate expected keys exist
            required_keys = {"answer", "confidence", "cited_chunks", "is_answerable"}
            missing = required_keys - set(parsed.keys())
            if missing:
                raise ValueError(f"Claude response missing keys: {missing}")

            # Add metadat not in Claude's response
            parsed["model_used"] = GENERATION_MODEL
            parsed["response_ms"] = elapsed_ms

            logger.info(
                f"Answer generated - confidence={parsed['confidence']}, "
                f"cited_chunks={parsed['cited_chunks']}, "
                f"response_ms={elapsed_ms}ms"
            )

            return parsed

        except (anthropic.APIError, anthropic.APIConnectionError) as e:
            last_error = str(e)
            if attempt < MAX_RETRIES:
                wait = BACKOFF_BASE**attempt
                logger.warning(
                    f"API error (attempt {attempt}): {e}. Retrying in {wait}s..."
                )
                time.sleep(wait)
            else:
                logger.error(f"API error after {MAX_RETRIES} attempts: {e}")

        except (json.JSONDecodeError, ValueError) as e:
            # Parse error are not retryable - Claude gave us bad output
            # Log the raw response for debugging
            logger.error(f"Response parse error: {e}")
            logger.error(f"Raw response: {raw_text[:500]}")
            raise RuntimeError(f"Failed to parse Claude response: {e}")

    raise RuntimeError(f"Claude API failed after {MAX_RETRIES} attempts: {last_error}")
