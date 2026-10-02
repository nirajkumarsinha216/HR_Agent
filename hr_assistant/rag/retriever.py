from hr_assistant.rag.embeddings import generate_embedding
from hr_assistant.rag.vector_store import (
    client,
    COLLECTION_NAME,
)


def search_policies(
    query: str,
    top_k: int = 5,
) -> list[dict]:

    query_embedding = generate_embedding(query)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=top_k,
    )

    retrieved_documents = []

    for result in results.points:

        retrieved_documents.append(
            {
                "text": result.payload["text"],
                "source": result.payload["source"],
                "chunk_id": result.payload["chunk_id"],
                "score": result.score,
            }
        )

    return retrieved_documents