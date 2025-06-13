# NLP Project Chatbot

Submission Date: 2025-06-13

Team Members:
- Bianca Burlacu (705366)
- Wojciech Kolasa (695344)
- Codrin Calin (696627)
- Salman Kanj (689581)

## Project Overview

This project presents an intelligent NLP-based chatbot designed to answer questions about the “Classifying Arrhythmia in Fighter Pilots” research for TNO. The system processes all project documentation—client info, research reports, data cleaning logs, model details, and presentations—to support interactive Q&A, context-following conversations, and information retrieval. The core NLP pipeline is built with **retrieval-augmented generation (RAG)** techniques implemented from scratch, focusing on document chunking, vector embeddings, and semantic similarity search. The chatbot is deployable via command line and runs entirely offline using local LLMs with Ollama.

---

## Installation

```bash
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage guide

Run the chatbot from the command line:

```bash
python app.py
```

You will be prompted to input a question. The chatbot processes the query, searches relevant document chunks, and returns a generated response using a locally hosted LLM.

## Architecture Description

The chatbot architecture consists of the following components:

1. **Document Preprocessing**:
   - Raw project files in `.docx` and `.pdf` format are converted to plain text and saved in `data/raw_txt/`.
   - A preprocessing script (`preprocessing.py`) cleans the text, filters by relevant sections (e.g., "Project 3"), and splits it into chunks of ~400 words with a 50-word overlap.
   - Each chunk is written to the `data/processed/` directory using the format `## Chunk N`.

2. **Embedding Generation**:
   - Each document chunk is embedded using the `all-MiniLM-L6-v2` model from the `SentenceTransformers` library. This model converts each chunk into a high-dimensional vector representation. The embeddings are stored as NumPy arrays along with metadata about the source file for efficient retrieval during question answering.
   - Resulting vectors are stored for later retrieval.

3. **Retrieval**:
   - User queries are embedded the same way.
   - Cosine similarity is used to find the most relevant document chunks.

4. **Answer Generation**:
   - The selected chunks + user query are passed to a local LLM via Ollama.
   - The model generates a response in natural language.

All components are custom-built except for the embedding model.

## NLP Approach Explanation

We implemented a simplified RAG (Retrieval-Augmented Generation) pipeline:

- **Chunking**: Raw documents are cleaned and split into word-based chunks (~400 words with 50-word overlap) using a preprocessing script. Each chunk is stored in the `data/processed/` folder with identifiers like `## Chunk 0`, `## Chunk 1`, etc. This preserves semantic context between overlapping segments.
- **Vector Search**: We compute embeddings for both chunks and queries and match them using cosine similarity.
- **Generation**: A local LLM is used to generate a response based on the retrieved context.

This design ensures:
- No external API calls
- Total privacy of the document content
- A realistic RAG implementation suitable for offline environments

## Known Limitations

- No web interface; only a command-line UI
- Does not support uploading new documents dynamically
- Limited conversational memory (not stateful beyond one turn)
- Chunking is naive and could be improved with better segmentation techniques