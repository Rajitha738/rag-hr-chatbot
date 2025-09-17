import faiss
import numpy as np
from utils import get_embeddings

# Load the FAISS index from file
def load_index(index_path="data/faiss_index.index"):
    try:
        index = faiss.read_index(index_path)
        return index
    except Exception as e:
        print(f"Error loading FAISS index: {e}")
        return None

# Retrieve top-k similar chunks
def retrieve(query: str, chunks: list, index, top_k: int = 3):
    if index is None:
        return ["Index not loaded"]

    # Get query embedding
    query_embedding = np.array([get_embeddings(query)], dtype=np.float32)

    # Search in FAISS
    D, I = index.search(query_embedding, top_k)

    # Return matching chunks
    results = []
    for idx in I[0]:
        if idx < len(chunks):
            results.append(chunks[idx])

    return results
