import os
import re

def clean_text(text):
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

def extract_project_section(text, project_title="Project Data & AI – Project 3"):
    start = text.find(project_title)
    if start == -1:
        # Project not found, return all text (fail gracefully)
        return text
    # Try to find the start of the next project to delimit the end
    possible_next = [
        "Project Data & AI – Project 4",
        "Project Data & AI – Project 5",
        "Project Data and AI – Project 4",
        "Project Data and AI – Project 5",
        "Project name:"
    ]
    # Find the first occurrence after start
    end = len(text)
    for next_proj in possible_next:
        idx = text.find(next_proj, start+1)
        if idx != -1 and idx < end:
            end = idx
    return text[start:end]

def chunk_text(text, chunk_size=400, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks

def preprocess_documents(raw_dir, processed_dir, chunk_size=400, overlap=50, only_project3=True):
    os.makedirs(processed_dir, exist_ok=True)
    for fname in os.listdir(raw_dir):
        path = os.path.join(raw_dir, fname)
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8", errors="ignore") as f:
            raw = f.read()
        cleaned = clean_text(raw)
        # Only filter for Project 3 for the combined file, or set only_project3=False to disable
        if only_project3 and "1-pagers" in fname:
            print(f"Filtering for Project 3 in {fname}")
            cleaned = extract_project_section(cleaned, "Project Data & AI – Project 3")
        chunks = chunk_text(cleaned, chunk_size, overlap)
        out_path = os.path.join(processed_dir, fname + ".chunks.txt")
        with open(out_path, "w", encoding="utf-8") as out_f:
            for idx, chunk in enumerate(chunks):
                out_f.write(f"## Chunk {idx}\n{chunk}\n")
        print(f"Processed {fname}: {len(chunks)} chunks.")

if __name__ == "__main__":
    preprocess_documents("data/raw_txt", "data/processed")
