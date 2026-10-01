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
        "ollama_chat/gemma4:12b-mlx"
    )

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "ollama_embedding/nomic-embed-text:latest"
    )

    COMPANY_NAME = os.getenv(
        "COMPANY_NAME",
        "LALA Company"
    )


settings = Settings()