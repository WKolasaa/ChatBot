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
