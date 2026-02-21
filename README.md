# RAG Chatbot (FastAPI + Streamlit + LangChain + Chroma)

A Retrieval-Augmented Generation (RAG) chatbot that lets you upload documents (PDF/TXT/MD), build an index, and chat with your content using retrieved context. Built with **FastAPI**, **Streamlit**, **LangChain**, and **Chroma**.

## Features

- Upload and ingest **PDF**, **TXT**, and **Markdown** documents
- Create embeddings and store them in **Chroma** (local vector database)
- Chat UI powered by **Streamlit**
- API layer with **FastAPI**
- Retrieval-based responses using relevant document chunks as context
- Simple, local-first workflow (great for prototyping and demos)

## Tech Stack

- **Backend API:** FastAPI
- **Frontend:** Streamlit
- **RAG Orchestration:** LangChain
- **Vector Store:** Chroma
- **Language:** Python

## Project Structure

> Update these paths to match your repository.

```text
.
├── app/                 # FastAPI app (routes, services)
├── ui/                  # Streamlit UI
├── data/                # Uploaded documents / local storage (optional)
├── chroma_db/           # Chroma persistence directory (optional)
├── requirements.txt
└── README.md
```

## Getting Started

### 1) Prerequisites

- Python 3.10+ recommended
- (Optional) `virtualenv` / `venv`

### 2) Installation

```bash
git clone https://github.com/AbdulRehman393/rag-chatbot.git
cd rag-chatbot

python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt
```

### 3) Configuration

Create a `.env` file (or export environment variables) as needed by your LLM provider.

Example:

```bash
# LLM provider key (choose what your project uses)
OPENAI_API_KEY=your_key_here

# Optional settings (adjust if your code supports them)
CHROMA_PERSIST_DIR=./chroma_db
```

> If you use a different provider (Groq, Gemini, Ollama, Azure OpenAI, etc.), rename variables accordingly.

### 4) Run the Backend (FastAPI)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs (if enabled):
- http://localhost:8000/docs

### 5) Run the Frontend (Streamlit)

```bash
streamlit run ui/app.py
```

Open:
- http://localhost:8501

## Usage

1. Start the backend and Streamlit UI
2. Upload one or more documents (PDF/TXT/MD)
3. Click **Index / Ingest** (based on your UI)
4. Ask questions in the chat
5. The assistant will answer using retrieved context from your documents

## Notes / Tips

- For best results, upload well-structured documents.
- If responses look off, try re-indexing after changing chunk size / overlap (if configurable).
- Persisting Chroma to disk helps avoid re-indexing on every restart.

## Roadmap (Optional)

- [ ] Add multi-user sessions
- [ ] Add citations/sources in answers
- [ ] Add Docker support
- [ ] Add evaluation scripts (RAGAS / custom metrics)

## Contributing

Contributions are welcome. Please open an issue to discuss significant changes before submitting a PR.

## License

Add your license here (e.g., MIT). If you haven’t added one yet, consider including a `LICENSE` file.
