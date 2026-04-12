"""
Chunker - Token-based text chunking service

The goal of this service:
    - Embedding models work bets with focused, consistently-sized text.
    - Overlap prevents context loss at chunk boundaries.
    - Token-based splitting ensures consistent sizes regardless of word lenght or special characters.

Key parameters:
    - CHUNK_SIZE : 1024 tokens - balanced of context richness vs precision
    - CHUNCK_OVERLAP: 128 tokens - 12.5% overlap bridges chunk boundaries
"""

import tiktoken
import tiktoken
import logging

# ===============================================================================
# Initialize tokenizer
# cl100k_base:
# - It's the encoding used by modern models
# - Voyage-3 uses a similar tokenization scheme
# - Consistent token counting ensures our chunck sizes are
# accurate relative to the embedding model's input limits.
# Load once at module level:
# - tiktoken.get_encoding() loads the enconding dictionary from disk.
# Doing it once at import time (not per call) avoids repeated I/O.
# This is the 'singleton' pattern - one instance shared across all function calls.
# ===============================================================================

ENCODER = tiktoken.get_encoding(
    "cl100k_base"
)  # gpt-4, gpt-3.5-turbo, text-embedding-3-small/large

logger = logging.getLogger(__name__)


def count_tokens(text: str) -> int:
    """
    Count the number of tokens in a text string.

    Why expose this as a separated function?

    - The /ingest endpoint needs token count for each chunk (stored in document_chunks.token_count).
    - Other services (generator.py) will need token counting for prompt budget calculation.
    - Single source of thruth - everyone uses the same encoder.

    Args:
        text : The text string to tokenize

    Returns:
        Number of tokens
    """
    return len(ENCODER.encode(text))


def chunk_text(
    text: str, chunk_size: int = 1024, chunk_overlap: int = 128
) -> list[dict]:
    """
    Split text into overlapping chunks based on token count.

    Algorithm:
        1. encode the entire text into tokens (list of integers).
        2. Slice a window of chunk_size tokens across the list.
        3. Each window step advances by (chunk_size - chunk_overlap) tokens.
        4. Decode each token window back to text.
        5. Returns list of chunk dicts with text, index, and token count.

    Why sliding window on tokens instead of splitting by sentences?
        - Sentence splitting produces inconsistent chunck sizes (some
         sentences are 5 tokens, others are 50).
        - The sliding window guarantees every chunk is exactly chunk_size
         tokens ( except the last one which may be shorter).
        - Overlap is mathematically precise . exactly 128 tokens shared
         between consecutive chunks.

    Why don't split mid-word:
        - tiktoken's decode() handles token bounderies cleanly.
        - A token always maps to complete characters (though not always
        complete words). In practice, splites mid-word ara rare and don't affect
        ambedding quality because the embedding model tokenizes the text on its own.

    Args:
        text : Full extracted text from a document
        chunk_size : Target tokens per chunck
        chunk_overlap : Overlapping tokens between consecutive chunks

    Returns:
        List of dicts, each with:
            - chunk_index (int): Position in document (0-based)
            - chunk_text (str): The text content
            - token_count (int): Actual token count for this chunk
    """

    # ============================================================================
    # Input validation
    # If someone passes chunk_overlap >= chunk_size, the sliding window never
    # advances and we get an infinite loop.
    # Fail fast with a clear message instead
    # ============================================================================

    if chunk_overlap >= chunk_size:
        raise ValueError(
            f"chunk_overlap ({chunk_overlap}) must be less than "
            f"chunk_size ({chunk_size}). "
            f"Recommended: overlap = 10-15% of chunk_size."
        )

    # 1. Encode entire text to tokens
    all_tokens = ENCODER.encode(text)
    total_tokens = len(all_tokens)

    logger.info(
        f"Chunking {total_tokens} tokens "
        f"(chunk_size={chunk_size}, overlap={chunk_overlap})"
    )

    # ============================================================================
    # Edge case: text is smaller than one chunk
    # A short document should still produce on chunk, not zero chunks.
    # ============================================================================

    if total_tokens <= chunk_size:
        logger.info("Text fits in single chunk - no splitting needed")
        return [
            {
                "chunk_index": 0,
                "chunk_text": text.strip(),
                "token_count": total_tokens,
            }
        ]

    # 2. Sliding window
    # stride = how fat the window moves each step
    # With chunk_size = 1024 and overlap = 128, stride = 896
    # So chunk 0 = tokens [0 : 1024], chunk 1 = [896 : 1920], ...
    # The last 128 tokens of chunk 0 are the first 128 of chunk 1

    stride = chunk_size - chunk_overlap
    chunks = []
    chunk_index = 0

    # ============================================================================
    # MAX_CHUNKS defensive cap
    # Prevents runaway chunking if something goes wrong.
    # A 500-page PDF at 1024 tokenS/chunk = ~500 chunks max.
    # 10,000 is a generous safety ceiling.
    # ============================================================================

    MAX_CHUNKS = 10000

    for start in range(0, total_tokens, stride):
        # Safety cap
        if chunk_index >= MAX_CHUNKS:
            logger.warning(
                f"Hit MAX_CHUNKS cap ({MAX_CHUNKS}). "
                f"Document may be unusually large. "
                f"Remaining text trunceted."
            )
            break
        # Extract token window
        end = min(start + chunk_size, total_tokens)
        chunk_tokens = all_tokens[start:end]

        # Decode tokens back to text
        chunk_text_str = ENCODER.decode(chunk_tokens).strip()

        # Skip empty chunks
        if not chunk_text_str:
            continue

        chunks.append(
            {
                "chunk_index": chunk_index,
                "chunk_text": chunk_text_str,
                "token_count": len(chunk_tokens),
            }
        )

        chunk_index += 1

        # ============================================================================
        # Stop condition : if this window reached the end of tokens
        # Without rhis, the last chunk might be very small (e.g. 10 tokens)
        # We still include it because those 10 tokens might contain
        # important information.
        # But the loop stops because there aren't more tokens to window over.
        # ============================================================================

        if end >= total_tokens:
            break

    logger.info(f"Chunking completed: {len(chunks)} chunks produced.")
    return chunks
