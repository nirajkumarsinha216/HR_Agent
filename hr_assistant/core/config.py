import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = os.getenv(
        "APP_NAME",
        "HR_Agent"
    )

    MODEL = os.getenv(
        "MODEL",
        "ollama_chat/qwen3:8b"
    )

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "nomic-embed-text:latest"
    )
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

    COMPANY_NAME = os.getenv(
        "COMPANY_NAME",
        "LALA Company"
    )


settings = Settings()