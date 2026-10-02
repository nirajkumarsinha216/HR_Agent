import ollama
import os

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434"
)

client = ollama.Client(
    host=OLLAMA_HOST
)


from hr_assistant.core.config import settings

def generate_embedding(text: str) -> list[float]:
    """
    Generate embeddings for the given text using Ollama API.

    Args:
        text (str): The input text to generate embeddings for.

    Returns:
        list[float]: The generated embeddings.
    """
    response = ollama.embed(model=settings.EMBEDDING_MODEL, input=text)
    return response['embeddings'][0]