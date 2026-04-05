# AI Knowledge Base Builder

An AI-powered knowledge base system that ingests documents (PDF, Markdown, plain text), extracts and chunks their content, generates embeddings, and enables semantic retrieval — turning a collection of files into a queryable knowledge base.

## Features

- **Multi-format ingestion** — supports PDF, Markdown (`.md`), and plain text (`.txt`)
- **Text extraction** — clean text extraction with encoding fallback and empty-file validation
- **Modular architecture** — services, routers, and middleware are fully separated

## Project Structure

```
project/
├── server/
│   ├── routers/        # API route handlers
│   ├── middleware/     # Request/response middleware
│   └── services/
│       └── extractor.py  # File type detection and text extraction
├── scripts/            # Utility scripts
├── uploads/            # Uploaded documents (not committed)
├── requirements.txt
└── .env.example        # Environment variable template
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Fabio-Ceriaco/ai-knowlege-base-builder.git
cd ai-knowlege-base-builder
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

## Environment Variables

| Variable | Description |
|---|---|
| *(more to be added as the project grows)* | |

## Supported File Types

| Format | MIME type | Extension |
|---|---|---|
| PDF | `application/pdf` | `.pdf` |
| Markdown | `text/markdown` | `.md` |
| Plain text | `text/plain` | `.txt` |

## License

MIT
