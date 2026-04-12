"""
Embedder - Voyage AI embeddings service
Converts text to 1024-dimensional vectors using voyage-3.5.

Why this service exists:
    - Single point of contact with Voyage AI - one place rto update if model or API changes.
    - Enforces input_type discipline (document vs query) at every call.
    - Validates uotput dimensions before returning to caller.
    - Implements retry logic for tarnsient API failures.


CRITICAL: input_type parameter
    - "document" -> use when embedding chunks for storage (ingestion)
    - "query" -> use when embedding a user question for search
        Voyage internally optimizes the mebedding space differently for
        each type, which materially improves retrieval accuracy.
"""

import voyageai
import os
import time
import logging
import voyageai

logger = logging.getLogger(__name__)

EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "voyage-3.5")
EXPECTED_DIMENSIONS = 1024

# Retry configuration
MAX_RETRIES = 3
BACKOFF_BASE = 2

# ============================================================================
# Voyage client
# ============================================================================

_client = voyageai.Client()

# Valid input_type values
VALID_IMPUT_TYPES = {"document", "query"}


def embed_texts(texts: list[str], input_type: str) -> list[list[float]]:
    """
    Embed list of texts using Voyage AI.

    Batch interface even for single texts:
        - The Voyage AI nativley accepts batches.
        - One function = one code path = fewer bugs.
        - Caller with one text just pass [text] and unwarp result[0].

    Input_typ as no default:
        - Forces the caller to make a deliberate semantic choice.
        - Prevents silent retrieval degradation from accidental defaults.


    Args:
        texts : List of strings to embed ( 1 or more)
        input_type : Must be "document" (for storage) or "query" (for search)

    Returns:
        List of embedding vectors, sema order as input texts.
        Each vector is a list of EXPECTED_DIMENSIONS(1024) floats.

    Raises:
        ValueError: On invalid input_type, empty input, or wrong dimansions.
        RuntimeError: After MAX_RETRIES failed attempts.
    """

    # 1. Input validation

    if input_type not in VALID_IMPUT_TYPES:
        raise ValueError(
            f"Invalid input_type='{input_type}'. "
            f"Must be one of: {VALID_IMPUT_TYPES}"
        )

    if not texts:
        raise ValueError("texts list is empty - nothing to embed.")

    if not all(isinstance(t, str) and t.strip() for t in texts):
        raise ValueError(
            "All texts must be non-empty strings. "
            "Empty or whitespace-only strings will produce useless embeddings."
        )

    logger.info(
        f"Embedding {len(texts)} text(s) "
        f"(model={EMBEDDING_MODEL}, input_type={input_type})"
    )

    # 2. Retry loop
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # The actual API call
            result = _client.embed(
                texts=texts, model=EMBEDDING_MODEL, input_type=input_type
            )

            embeddings = result.embeddings

            # 3. Dimension validation

            if len(embeddings) != len(texts):
                raise ValueError(
                    f"Voyage returned {len(embeddings)} embeddings "
                    f"for {len(texts)} input texts - count mismatch."
                )
            for i, vec in enumerate(embeddings):
                if len(vec) != EXPECTED_DIMENSIONS:
                    raise ValueError(
                        f"Embeddung {i} has {len(vec)} dimensions, "
                        f"expected {EXPECTED_DIMENSIONS}."
                        f"Model '{EMBEDDING_MODEL}' may be misconfigured."
                    )
            logger.info(
                f"Embedding sucessful: {len(embeddings)} vectors "
                f"x {EXPECTED_DIMENSIONS} dims (attempt {attempt})"
            )
            return embeddings
        except ValueError:
            # Dimension/validation errors - don't retry, these are bugs
            # not transient failures. Re-raise immediately.
            raise

        except Exception as e:
            # Network errors, rate limits, transient API issues - retry
            last_error = e
            logger.warning(
                f"Embedding attempt {attempt}/{MAX_RETRIES} failed: "
                f"{type(e).__name__}: {e}"
            )

            if attempt < MAX_RETRIES:
                wait_seconds = BACKOFF_BASE**attempt
                logger.info(f"Retrying in {wait_seconds}s...")
                time.sleep(wait_seconds)

    raise RuntimeError(
        f"Embedding failed after {MAX_RETRIES} attempts. "
        f"Last error: {type(last_error).__name__}: {last_error}"
    )


def embed_single(text: str, input_type: str) -> list[float]:
    """
    Comvenience wrapper to embed exactly one text.

    This exists alongside embed_texts:
        - The /ask endpoint embeds exactly one question per call.
        - Callers shouldn't have to remember to warp in [text] and unwarp[0].
        - Internally calls embed_texts to keep one source of truth.

    Args:
        text: Single string to embed.
        input_type: "document" or "query"

    Returns:
        Single embedding vector (list of 1024 floats).
    """

    result = embed_texts([text], input_type=input_type)
    return result[0]
