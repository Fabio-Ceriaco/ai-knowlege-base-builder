"""
Extractor - Text extraction service
Handles PDF, Markdown, and plain text files.
Return clean text string ready for chunking.

Why exists this service:
- Single responsibility: one file type -> one extraction method
- Quality gate: clean text = good embeddings = accurate retrieval
- Isolated: no knowledge of chunks, embeddings, or database
"""

import fitz  # PyMuPDF
import logging

# ============================================================================
# CONFIGURE LOGGING
# Every service should log its operations. When something
# breaks in production, logs are the first debugging tool.
# Model-level logger used so each service identifies itself.
# ============================================================================

logger = logging.getLogger(__name__)

# ============================================================================
# Supported files types - used for validation
# Fail fast with a clear error rather than letting an
# unsupported file type pass through and produce garbage output.
# ============================================================================

SUPPORTED_TYPES = {
    "application/pdf": "pdf",
    "text/markdown": "markdown",
    "text/plain": "text",
}

# ============================================================================
# Also map by file extension as a fallback
# Some uploads form clients send generic content types like
# 'application/octet-stream'. Extension mapping catches those.
# ============================================================================

EXTENSION_MAP = {
    ".pdf": "pdf",
    ".md": "markdown",
    ".txt": "text",
}


def detect_source_type(file_name: str, content_type: str = None) -> str:
    """
    Determine the file type from content_typr header or file extension.

    Two detection methods:
        - content_type comes from the HTTP upload header (most reliable)
            whene the client sets it correctly.
        - extension fallback handles cases where content_type is missing
            or generic (e.g. 'application/octet-stream' form curl)

    Args:
        file_name: Original filename (e.g 'document.pdf')
        content_type: MIME type from upload header (e.g. 'application/pdf')

    Returns:
        Source type string: 'pdf', 'markdown', or 'text'

    Raises:
        ValueError: If file type is not supported
    """

    # Try content_type first

    if content_type and content_type in SUPPORTED_TYPES:
        return SUPPORTED_TYPES[content_type]

    # Fallback to file extension
    ext = "." + file_name.rsplit(".", 1)[-1].lower() if "." in file_name else ""
    if ext in EXTENSION_MAP:
        return EXTENSION_MAP[ext]

    # Neither method worked - reject the file
    raise ValueError(
        f"Unsupported file type: content_type='{content_type}', "
        f"filename='{file_name}'. "
        f"Supported: PDF, Markdown (.md), Plain text (.txt)"
    )


def extract_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from a PDF file using PyMuPDF.

    Page-by-page extraction:
        - PyMuPDF's get_text() returns text per page with proper reading order.
        - Joining with double newlines perserves page boundaries.
        - The chunker uses these boundaries as natural split points.

    strip() each page:
        - Removes leading/trailing whitespace and empty lines per page.
        - Prevents chunks that are mostly whitespace.


    Args:
        file_bytes: Raw PDF file content as bytes

    Returns:
        Estracted text as a single string, pages sparated by double newlines.

    Raises:
        ValueError: If PDF has no extractable text (e.g. scanned image PDF)
    """

    try:
        # fitz.open() accepts bytes via stream paramter + filetype
        doc = fitz.open(stream=file_bytes, filetype="pdf")

        pages = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text().strip()
            if text:  # Skip empty pages
                pages.append(text)
        doc.close()

        # Validate if something got
        if not pages:
            raise ValueError(
                "PDF contains no extractable text. "
                "It may be a scanned document. "
                "ORC is not supported in this version."
            )

        full_text = "\n\n".join(pages)
        logger.info(
            f"PDF extraction completed: {len(pages)} pages, {len(full_text)} chars."
        )
        return full_text

    except fitz.FileDataError as e:
        # PyMuPDF couldn't parse the file
        raise ValueError(f"Invalid or corrupted PDF file: {e}")


def extract_form_text(file_bytes: bytes) -> str:
    """
    Extract text from a plain text or markdoen file.

    More simple:
        - .text and .md files are already text - no parsing needed.
        - Just need decode bytes to string and strip whitespaces.
        - Markdown formatting is preserved beacuse the chunker and
            embedder work on raw text. Claude handler markdown natively.

    Try utf-8 then latin-1:
        - utf-8 covers ~98% of text files.
        - latin-1 is a fallback that never fails because it
            maps every byte value 0-255 to a character. It may produce
            worng characters for non-latin scripts, but ut won't crash.
        - This is a production approach pattern - always have a fallback encoding.

    Args:
        file_bytes: Raw file content as bytes

    Returns:
        Decoded text string

    Reise:
        ValueError: If file is empty after decoding
    """

    # Try UTF-8 first
    try:
        text = file_bytes.decode("utf-8").strip()
    except UnicodeDecodeError:
        # Fallback to latin-1
        logger.warning("UTF-8 decode failed, falling back to latin-1")
        text = file_bytes.decode("latin-1").strip()

    if not text:
        raise ValueError("File is empty - no text content found.")

    logger.info(f"Text extraction completed: {len(text)} chars.")
    return text


def extract_text(file_bytes: bytes, file_name: str, content_type: str = None) -> dict:
    """
    Main entry point - detects file type and routes to the correct extractor.

    Return a dict insted of just the text string:
        - The /ingest endpoint needs metadata (source_type, char count)
            to write the documents table row
        - Returning a dict with text + metadata avoids the caller having
            to re-detect the file type or re-count characters.
        - This is the 'object parameter passing' pattern from code style.

    Args:
        file_bytes: Raw file content as bytes
        file_name: Original filename for type detection
        content_type: MIME type from uploaded header

    Returns:
        dict with keys:
            - text (str): Extracted text content
            - source_type (str): 'pdf', 'markdown', 'text'
            - char_count (int): Lenght of extracted text
            - file_name (str): Original filename (passed throught)
            - file_size_bytes (int): Size of original file in bytes
    """

    # Detect file type
    source_type = detect_source_type(file_name, content_type)
    logger.info(f"Extracting from '{file_name}' (type: {source_type})")

    # Route to the correct extractor

    if source_type == "pdf":
        text = extract_from_pdf(file_bytes)
    else:
        # Both 'markdown' and 'text' are plain text
        text = extract_form_text(file_bytes)

    # Return text + metadata as a dict
    return {
        "text": text,
        "source_type": source_type,
        "char_count": len(text),
        "file_name": file_name,
        "file_size_bytes": len(file_bytes),
    }
