import os
from dotenv import load_dotenv


class Config:

    load_dotenv()

    WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
    VOYAGE_EMBED_MODEL = os.getenv("VOYAGE_EMBED_MODEL")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    TOP_K = os.getenv("TOP_K", "5")
    GAP_THRESHOLD = os.getenv("GAP_THRESHOLD", "0.80")
    GENERATION_MODEL = os.getenv("GENERATION_MODEL", "claude-sonnet-4-6")


settings = Config()
