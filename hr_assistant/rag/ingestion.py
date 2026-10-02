from pathlib import Path

from pypdf import PdfReader

from hr_assistant.rag.chunking import chunk_text
from hr_assistant.rag.embeddings import generate_embedding
from hr_assistant.rag.vector_store import (
    create_collection,
    insert_chunks,
)


POLICY_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "policies"
)


def load_pdf(file_path: Path) -> str:

    reader = PdfReader(str(file_path))

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def ingest_policies():

    all_chunks = []

    for pdf_file in POLICY_DIR.glob("*.pdf"):

        print(f"Processing: {pdf_file.name}")

        document_text = load_pdf(pdf_file)

        chunks = chunk_text(document_text)

        for chunk_number, chunk in enumerate(chunks):

            embedding = generate_embedding(chunk)

            all_chunks.append(
                {
                    "text": chunk,
                    "embedding": embedding,
                    "source": pdf_file.name,
                    "chunk_id": chunk_number,
                }
            )

    if not all_chunks:
        print("No policy documents found.")

        return

    vector_size = len(
        all_chunks[0]["embedding"]
    )

    create_collection(vector_size)

    insert_chunks(all_chunks)

    print(
        f"Indexed {len(all_chunks)} chunks "
        f"from HR policy documents."
    )


if __name__ == "__main__":
    ingest_policies()