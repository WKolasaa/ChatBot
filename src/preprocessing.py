import os
import re

def clean_text(text):
    # Basic cleaning: remove extra whitespace, simple headers/footers
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

def chunk_text(text, chunk_size=400, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks

def preprocess_documents(raw_dir, processed_dir, chunk_size=400, overlap=50):
    os.makedirs(processed_dir, exist_ok=True)
    for fname in os.listdir(raw_dir):
        path = os.path.join(raw_dir, fname)
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8", errors="ignore") as f:
            raw = f.read()
        cleaned = clean_text(raw)
        chunks = chunk_text(cleaned, chunk_size, overlap)
        out_path = os.path.join(processed_dir, fname + ".chunks.txt")
        with open(out_path, "w", encoding="utf-8") as out_f:
            for idx, chunk in enumerate(chunks):
                out_f.write(f"## Chunk {idx}\n{chunk}\n")
        print(f"Processed {fname}: {len(chunks)} chunks.")

if __name__ == "__main__":
   preprocess_documents("data/raw_txt", "data/processed")

