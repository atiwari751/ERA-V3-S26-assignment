import time
import numpy as np
from vector_index import faiss_index, page_metadata, embedding_dimension
from utils import get_embedding

async def index_page(url: str, text: str) -> int:
    """
    Computes an embedding for the provided page text using the external
    'nomic-embed-text' model (via get_embedding), adds it to the FAISS index,
    and stores the page metadata.
    
    Returns:
        The new document's index ID.
    """
    vector = get_embedding(text)
    if vector.shape[0] != embedding_dimension:
        raise ValueError("Embedding dimension mismatch.")
    
    # Convert to 2D array: FAISS expects a 2D numpy array of type float32.
    vector = np.expand_dims(vector, axis=0)  # shape: (1, embedding_dimension)
    faiss_index.add(vector)  # Adds the vector to the FAISS index
    
    # The new document ID is its position in our metadata list.
    idx = len(page_metadata)
    page_metadata.append({
        "url": url,
        "text": text,
        "timestamp": time.time()
    })
    
    print(f"Indexed page: {url} with FAISS ID: {idx}")
    return idx
