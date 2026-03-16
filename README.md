# 📅 AI Medical Assistant Chatbot — RAG-based Application





---

## 🧠 Project Overview

This application is a **Medical Domain Chatbot** built using **Retrieval-Augmented Generation (RAG)**. It allows users to upload their own medical documents (e.g., textbooks, reports), and the system intelligently answers queries by retrieving the most relevant content before generating a final response.

---

## 🎓 What is RAG?

**RAG (Retrieval-Augmented Generation)** enhances language models by supplying relevant external context from a knowledge base, preventing hallucinations and improving accuracy, especially for factual or specialized domains like **medicine**.

---

## 🔄 Architecture

```
User Input
   ↓
Query Embedding → Pinecone Vector DB ← Embedded Chunks ← Chunking ← PDF Loader
   ↓
Retrieved Docs
   ↓
     RAG Chain (Groq + LangChain)
   ↓
LLM-generated Answer
```



---

## 📚 Features

- Upload medical PDFs (notes, books, etc.)
- Auto-extracts text and splits into semantic chunks
- Embeds using Ollama Embeddings embeddings
- Stores vectors in **Pinecone DB**
- Uses **Groq** via LangChain
- FastAPI backend with endpoints for file upload and Q\&A


GROQ_API_KEY=...
PINECONE_API_KEY=...


## 🌐 Deployment

- Hosted on [Render](https://render.com)
- **Root Directory**: leave blank (repo root).
- **Start Command** (use this exactly):
  ```bash
  export PYTHONPATH="$(pwd)" && poetry run uvicorn main:app --host 0.0.0.0 --port $PORT
  ```
  Ensure **Root Directory** is blank so this runs from the repo root (where `main.py` and `server/` are).

---

## 🌟 Credits


- Inspired by LangChain, Groq, Pinecone, and FastAPI ecosystems
