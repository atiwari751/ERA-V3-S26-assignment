import faiss
import numpy as np

# Define the embedding dimensionality (must match your embedding model's output).
embedding_dimension = 768

# Create a FAISS index using L2 (Euclidean) distance.
# IndexFlatL2 is a straightforward in‑memory flat index.
faiss_index = faiss.IndexFlatL2(embedding_dimension)

# In‑memory list to maintain page metadata (e.g., URL, text, timestamp).
page_metadata = []
