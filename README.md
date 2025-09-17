# RAG HR Chatbot

An **HR Policy Chatbot** built with **FastAPI**, **Streamlit**, and **FAISS** that lets employees query company HR policies from a PDF document.  
It uses **Sentence Transformers** to embed policy text and retrieves relevant answers using **Retrieval-Augmented Generation (RAG)**.

---

## Features
- Upload and process HR policy PDFs
- Retrieve policy answers using FAISS vector search
- FastAPI backend for embeddings + retrieval
- Streamlit frontend for user-friendly chat interface
- Docker support for easy deployment

---

## Project Structure

rag-hr-chatbot/

│── backend/ # FastAPI app

│ ├── app.py # API endpoints

│ ├── utils.py # PDF + text processing

│ ├── retriever.py # FAISS index + retrieval

│ ├── cache.py # Simple cache layer

│ └── init.py
│
│── frontend/ # Streamlit app

│ └── streamlit_app.py
│
│── data/ # HR-Policy.pdf 

│── requirements.txt

│── Dockerfile

│── README.md

│── .gitignore

