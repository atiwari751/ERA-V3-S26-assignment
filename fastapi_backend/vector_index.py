import faiss
import numpy as np
import time
from utils import get_embedding

# Define the embedding dimensionality (must match your embedding model's output).
embedding_dimension = 768

# Create a FAISS index using L2 (Euclidean) distance.
# IndexFlatL2 is a straightforward in‑memory flat index.
faiss_index = faiss.IndexFlatL2(embedding_dimension)

# In‑memory list to maintain page metadata (e.g., URL, text, timestamp).
page_metadata = []

async def index_page(url: str, text: str) -> int:
    print(f"[Indexing] Attempting to index page for URL: {url[:50]}...")
    vector = get_embedding(text)
    print(f"[Indexing] Obtained embedding of shape: {vector.shape}")

    if vector.shape[0] != embedding_dimension:
        raise ValueError(f"Embedding dimension mismatch: expected {embedding_dimension}, but got {vector.shape[0]}")
    
    # Convert to 2D array: FAISS expects shape (1, embedding_dimension)
    vector = np.expand_dims(vector, axis=0)
    # Add the vector to FAISS index
    faiss_index.add(vector)
    
    # Add to page metadata
    idx = len(page_metadata)
    page_metadata.append({
        "url": url,
        "text": text,
        "timestamp": time.time()
    })
    print(f"[Indexing] Successfully indexed page with FAISS ID: {idx}")
    print(f"[Indexing] Total indexed pages: {len(page_metadata)}")
    return idx
