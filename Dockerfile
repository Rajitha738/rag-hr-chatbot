# Use official Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies (for FAISS, PyTorch, etc.)
RUN apt-get update && apt-get install -y \
    gcc g++ libglib2.0-0 libsm6 libxrender1 libxext6 git wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into container
COPY . .

# Expose ports for backend and frontend
EXPOSE 8000
EXPOSE 8501

# Start both FastAPI (backend) and Streamlit (frontend)
CMD ["bash", "-c", "uvicorn backend.app:app --host 0.0.0.0 --port 8000 & streamlit run frontend/streamlit_app.py --server.port=8501 --server.address=0.0.0.0"]
