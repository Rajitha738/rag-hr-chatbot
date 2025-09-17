from fastapi import FastAPI
from pydantic import BaseModel
from backend.utils import extract_text, clean_text, chunk_text, get_embeddings, build_faiss_index
from backend.retriever import load_index_and_chunks, retrieve
from backend.cache import get_cached, set_cache
from sentence_transformers import SentenceTransformer
import pickle
import faiss
import os

# Create FastAPI app
app = FastAPI()

# Allow CORS (for frontend connection)
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all during dev
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize FAISS index and chunks
if not os.path.exists("data/hr_policy_faiss.index"):
    text = extract_text("data/HR-Policy.pdf")
    clean = clean_text(text)
    chunks = chunk_text(clean)
    embeddings = get_embeddings(chunks)
    index = build_faiss_index(embeddings)

    # Save index and chunks
    faiss.write_index(index, "data/hr_policy_faiss.index")
    with open("data/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)
else:
    index, chunks = load_index_and_chunks("data/hr_policy_faiss.index", "data/chunks.pkl")

# Define request body
class Query(BaseModel):
    question: str

# API endpoint
@app.post("/query")
def get_answer(q: Query):
    cached = get_cached(q.question)
    if cached:
        return {"answer": cached}

    retrieved_chunks = retrieve(q.question, index, chunks, model)
    answer = "\n".join(retrieved_chunks)

    set_cache(q.question, answer)
    return {"answer": answer}
