import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "IS-SARATHI Indian Standards Recommendation System")
    API_V1_PREFIX: str = os.getenv("API_V1_PREFIX", "/api/v1")
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))

    # CORS
    ALLOWED_ORIGINS: str = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173",
    )

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

    # Security & JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change-me-in-production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    # Database - dynamically resolved relative to backend directory
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'is_sarathi.db').replace('\\', '/')}",
    )

    # Redis Cache
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_ENABLED: bool = os.getenv("REDIS_ENABLED", "true").lower() == "true"

    # Google Gemini LLM
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    # Pinecone Vector DB
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "is-sarathi-standards")

    # Hugging Face Embeddings
    EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")

    # Free/open document storage (default local, optional self-hosted S3-compatible storage)
    STORAGE_PROVIDER: str = os.getenv("STORAGE_PROVIDER", "local").lower()
    STORAGE_ENDPOINT_URL: str = os.getenv("STORAGE_ENDPOINT_URL", "")
    STORAGE_ACCESS_KEY_ID: str = os.getenv("STORAGE_ACCESS_KEY_ID", os.getenv("AWS_ACCESS_KEY_ID", ""))
    STORAGE_SECRET_ACCESS_KEY: str = os.getenv("STORAGE_SECRET_ACCESS_KEY", os.getenv("AWS_SECRET_ACCESS_KEY", ""))
    STORAGE_REGION: str = os.getenv("STORAGE_REGION", os.getenv("AWS_REGION", "us-east-1"))
    STORAGE_BUCKET: str = os.getenv("STORAGE_BUCKET", os.getenv("AWS_S3_BUCKET", "is-sarathi-documents"))
    USE_LOCAL_STORAGE: bool = (
        os.getenv("USE_LOCAL_STORAGE", "true").lower() == "true"
        or STORAGE_PROVIDER == "local"
    )
    LOCAL_STORAGE_DIR: str = os.getenv("LOCAL_STORAGE_DIR", "./storage/documents")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

settings = Settings()
