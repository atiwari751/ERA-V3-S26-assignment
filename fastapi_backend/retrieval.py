import numpy as np
from vector_index import faiss_index, page_metadata, embedding_dimension
from utils import get_embedding

async def query_pages(query: str, topK: int = 3):
    """
    Computes an embedding for the provided query using the external
    'nomic-embed-text' model, then uses the FAISS index to find the top K
    closest matching pages.
    
    Returns:
        A list of page metadata dictionaries for the matching pages.
    """
    print(f"[Retrieval] Processing query: {query}")
    query_vector = get_embedding(query)
    print(f"[Retrieval] Query embedding shape: {query_vector.shape}")
    if query_vector.shape[0] != embedding_dimension:
        raise ValueError("Query embedding dimension mismatch.")
    
    query_vector = np.expand_dims(query_vector, axis=0)
    # Perform search on the FAISS index.
    distances, indices = faiss_index.search(query_vector, topK)
    print(f"[Retrieval] FAISS search returns distances: {distances} and indices: {indices}")
    
    results = []
    # indices is a 2D array with shape (1, topK)
    for idx in indices[0]:
        if idx != -1 and idx < len(page_metadata):
            results.append(page_metadata[idx])
            print(f"[Retrieval] Found page metadata for index {idx}")
    print(f"[Retrieval] Returning {len(results)} results")
    return results
