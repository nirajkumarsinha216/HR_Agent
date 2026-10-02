from pathlib import Path
import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

VECTOR_DB_PATH = Path(__file__).resolve().parent.parent / ".qdrant"

QDRANT_URL = os.getenv(
    "QDRANT_URL",
    "http://localhost:6333"
)

COLLECTION_NAME = "hr_policies"

client = QdrantClient(
    url=QDRANT_URL
)

def create_collection(vector_size: int) -> None:
    """
    Create a collection in the Qdrant vector store.

    Args:
        vector_size (int): The size of the vectors to be stored in the collection.
    """
    collections = client.get_collections()

    existing_collections = [collection.name for collection in collections.collections]

    if COLLECTION_NAME not in existing_collections:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

def insert_chunks(chunks: list[dict],):
    """
    Insert chunks of text into the Qdrant vector store.

    Args:
        chunks (list[dict]): A list of dictionaries containing chunk data.
    """
    points = []

    for index, chunk in enumerate(chunks):
        point = PointStruct(
            id=index,
            vector=chunk["embedding"],
            payload={"text": chunk["text"], "source": chunk.get("source", ""),"chunk_id": chunk.get("chunk_id", "")},
        )
        points.append(point)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )