import ollama
from .vector_db import VectorDB
from .embeddings import EmbeddingModel

class Chatbot:
    def __init__(self, vector_store_dir, embedding_model, model_name="llama3"):
        self.db = VectorDB(vector_store_dir)
        self.embedder = embedding_model
        self.model_name = model_name
        self.history = []

    def ask(self, question, top_k=5):
        q_emb = self.embedder.encode([question])[0]
        docs = self.db.similarity_search(q_emb, top_k=top_k)
        context = "\n\n".join([f"Source: {d['meta']['source_file']}\n{d['chunk']}" for d in docs])
        prompt = self.build_prompt(question, context)
        response = ollama.chat(model=self.model_name, messages=[
            {"role": "system", "content": "You are an expert assistant for a university project about arrhythmia detection in F-35 pilots."},
            {"role": "user", "content": prompt}
        ])["message"]["content"]
        self.history.append({"question": question, "answer": response})
        return response

    def build_prompt(self, question, context):
        return (
            "Use the following project information and answer the user's question. "
            "If the answer is not present, state so clearly.\n\n"
            f"PROJECT CONTEXT:\n{context}\n\n"
            f"USER QUESTION: {question}\n\n"
            "Provide a clear and concise answer."
        )

    def show_history(self):
        for turn in self.history:
            print(f"Q: {turn['question']}\nA: {turn['answer']}\n{'-'*40}")
