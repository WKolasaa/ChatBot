import os
from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingModel:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        # Returns numpy array
        return self.model.encode(texts, show_progress_bar=False)

def build_embeddings(processed_dir, vector_store_dir, model_name="all-MiniLM-L6-v2"):
    os.makedirs(vector_store_dir, exist_ok=True)
    model = EmbeddingModel(model_name)
    all_chunks = []
    meta = []

    # Loop through processed docs
    for fname in os.listdir(processed_dir):
        path = os.path.join(processed_dir, fname)
        with open(path, encoding="utf-8") as f:
            lines = f.read().split("## Chunk ")
            for line in lines[1:]:
                chunk_body = "\n".join(line.split("\n")[1:])
                all_chunks.append(chunk_body)
                meta.append({"source_file": fname})

    embeddings = model.encode(all_chunks)
    np.save(os.path.join(vector_store_dir, "embeddings.npy"), embeddings)
    with open(os.path.join(vector_store_dir, "chunks.txt"), "w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(chunk + "\n---\n")
    import json
    with open(os.path.join(vector_store_dir, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f)
    print(f"Saved {len(all_chunks)} chunks with embeddings.")

if __name__ == "__main__":
    build_embeddings("data/processed", "data/vector_store")
