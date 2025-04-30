import requests
import numpy as np

# Must match the dimension used in vector_index.py.
embedding_dimension = 768

def get_embedding(text: str) -> np.ndarray:
    """
    Obtain an embedding for the provided text by calling an external
    embedding API that is expected to use the "nomic-embed-text" model.
    
    Returns:
        A numpy array (float32) representing the embedding.
    If the external API call fails, a random embedding is returned.
    """
    embed_api_url = "http://localhost:11434/api/embeddings"
    payload = {
        "model": "nomic-embed-text",  # Specify the model to use
        "prompt": text
    }
    try:
        response = requests.post(embed_api_url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        embedding = np.array(data.get("embedding"), dtype="float32")
        if embedding.shape[0] != embedding_dimension:
            raise ValueError("Returned embedding dimension does not match expectation.")
        return embedding
    except Exception as e:
        print(f"Error calling the embedding API: {e}")
        # Fallback: generate a random embedding, useful for demonstration
        return np.random.rand(embedding_dimension).astype("float32")
