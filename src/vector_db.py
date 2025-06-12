import numpy as np
import json
import os

def cosine_similarity(a, b):
    a_norm = a / (np.linalg.norm(a) + 1e-8)
    b_norm = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-8)
    return np.dot(b_norm, a_norm)

class VectorDB:
    def __init__(self, vector_store_dir):
        self.embeddings = np.load(os.path.join(vector_store_dir, "embeddings.npy"))
        with open(os.path.join(vector_store_dir, "chunks.txt"), encoding="utf-8") as f:
            self.chunks = f.read().split("\n---\n")[:-1]
        with open(os.path.join(vector_store_dir, "meta.json"), encoding="utf-8") as f:
            self.meta = json.load(f)

    def similarity_search(self, query_emb, top_k=5):
        sims = cosine_similarity(query_emb, self.embeddings)
        idxs = np.argsort(sims)[-top_k:][::-1]
        results = []
        for i in idxs:
            results.append({
                "chunk": self.chunks[i],
                "similarity": float(sims[i]),
                "meta": self.meta[i]
            })
        return results
