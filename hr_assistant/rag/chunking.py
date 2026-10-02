def chunk_text(text: str, chunk_size: int = 800, chunk_overlap: int = 100) -> list[str]:
    """
    Chunk the input text into smaller segments.

    Args:
        text (str): The input text to be chunked.
        chunk_size (int): The maximum size of each chunk.
        chunk_overlap (int): The number of overlapping characters between chunks.

    Returns:
        list[str]: A list of text chunks.
    """
    text = text.strip()
    if not text:
        return []
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - chunk_overlap
    return chunks