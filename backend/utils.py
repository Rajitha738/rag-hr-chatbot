import re
from typing import List, Dict
from pypdf import PdfReader

def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def load_pdf_to_chunks(pdf_path: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[Dict]:
    """
    Read PDF, return list of chunks: [{'id': int, 'text': str, 'meta': {...}}, ...]
    """
    reader = PdfReader(pdf_path)
    pages = []
    for pageno, page in enumerate(reader.pages):
        try:
            txt = page.extract_text() or ""
        except Exception:
            txt = ""
        pages.append(clean_text(txt))

    # join with page boundaries
    joined = "\n\n".join(pages)
    tokens = joined.split()  # rough splitting
    chunks = []
    i = 0
    chunk_id = 0
    while i < len(tokens):
        piece = tokens[i:i+chunk_size]
        text = " ".join(piece)
        if text.strip():
            chunks.append({
                "id": chunk_id,
                "text": clean_text(text),
                "meta": {"source": pdf_path, "chunk_id": chunk_id}
            })
            chunk_id += 1
        i += chunk_size - chunk_overlap
    return chunks

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "data/HR-Policy.pdf"
    chunks = load_pdf_to_chunks(path)
    print(f"Loaded {len(chunks)} chunks from {path}")
    if chunks:
        print(chunks[0]["text"][:400])
