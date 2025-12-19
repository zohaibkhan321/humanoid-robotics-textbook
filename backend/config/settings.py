from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API Keys
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    # Database URLs
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key: Optional[str] = os.getenv("QDRANT_API_KEY")
    qdrant_local_path: Optional[str] = os.getenv("QDRANT_LOCAL_PATH", "/tmp/qdrant_data_new")
    neon_conn: str = os.getenv("NEON_CONN", "")

    # Application settings
    cors_origins: List[str] = ["http://localhost:3000", "https://yourdomain.com"]
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    rate_limit_window: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # in seconds

    # Model settings
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "embed-english-v3.0")
    embedding_input_type: str = os.getenv("EMBEDDING_INPUT_TYPE", "search_document")
    generation_model: str = os.getenv("GENERATION_MODEL", "command-r-plus")

    # Vector database settings
    collection_name: str = os.getenv("COLLECTION_NAME", "documents")

    # Text processing settings
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "500"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "50"))

    # RAG Configuration
    default_top_k: int = int(os.getenv("DEFAULT_TOP_K", "5"))
    max_chunk_tokens: int = int(os.getenv("MAX_CHUNK_TOKENS", "1000"))
    max_query_length: int = int(os.getenv("MAX_QUERY_LENGTH", "1000"))
    max_selected_text_length: int = int(os.getenv("MAX_SELECTED_TEXT_LENGTH", "5000"))

    # Development Settings
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "info")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"


settings = Settings()