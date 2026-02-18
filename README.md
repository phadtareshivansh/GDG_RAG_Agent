GDG RAG Workshop — Retrieval-Augmented Generation (RAG) Demo
===========================================================

A small educational project that demonstrates a Retrieval-Augmented Generation (RAG) system using:

- A lightweight local Knowledge Base built on ChromaDB
- Text chunking utilities for document ingestion
- A defensive Gemini (Google) wrapper for generation (uses `google.genai` when available)
- A Streamlit web interface for uploading documents, fetching live web pages, and chatting with the RAG agent

This repository is a hands-on workbook for learning how retrieval + generation are combined to build accurate, source-citing assistants.

Contents
--------
- `Day-1/` — Text processing exercises (cleaning, similarity, FAQ finder)
- `Day-2/` — Knowledge base and chunking utilities (ChromaDB + fallback embeddings)
- `Day-3/` — RAG agent, Gemini wrapper, and Streamlit app

Quick status
------------
- Knowledge base now supports a deterministic fallback embedding function when sentence-transformers / PyTorch are unavailable.
- The Gemini wrapper will work if `google.genai` is installed and `GEMINI_API_KEY` is set. Otherwise it returns a diagnostic but still allows the retrieval pipeline to operate.

Requirements
------------
- Python 3.10+ (3.11 used in development)
- pip

Python packages (install via requirements.txt):
- streamlit
- chromadb
- sentence-transformers (optional, for higher-quality embeddings)
- google-genai (optional, for Gemini generation)
- requests, beautifulsoup4, python-dotenv, numpy, pandas, pytest

Installation
------------
1. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate  # zsh / bash
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Optional: If you want high-quality local embeddings, install a compatible PyTorch + sentence-transformers. On macOS (CPU-only) you can try:

```bash
pip install "torch>=2.4.0" --extra-index-url https://download.pytorch.org/whl/cpu
pip install -U sentence-transformers
```

If you do not install these, the project uses a deterministic fallback embedding so the knowledge base and retrieval still work.

Environment
-----------
Create a `.env` file in the repository root with your Gemini API key (optional):

```
GEMINI_API_KEY=your_gemini_api_key_here
```

The Streamlit UI also accepts a Gemini API key in the sidebar.

How to run
----------
Start the Streamlit app (recommended):

```bash
streamlit run Day-3/streamlit_app.py --server.port 8501 --server.address 127.0.0.1
```

Open your browser at `http://localhost:8501`.

Notes for running:
- If you see `ERR_CONNECTION_REFUSED` in the browser, ensure the server is running and listening on `127.0.0.1:8501`.
- Keep the terminal window open to watch logs and exceptions.

Quick programmatic smoke test (non-LLM)
--------------------------------------
This creates a KnowledgeBase, adds a short document and queries it (works even without Gemini):

```bash
python3 - <<'PY'
import sys, os
cwd = '/path/to/repo'  # replace
sys.path.insert(0, os.path.join(cwd, 'Day-2'))
from knowledge_base import KnowledgeBase
kb = KnowledgeBase('quick_check')
kb.add_document('GDG events are free and run 9:00-17:00. Bring laptop.', metadata={'source':'quick'})
res = kb.query('When do workshops run?')
print('Found', len(res), 'results. First metadata:', res[0]['metadata'])
PY
```

Developer notes / troubleshooting
--------------------------------
- If `knowledge_base` import fails with a SyntaxError, check for stray characters at the file top (the workbook includes docstrings). This repo fixes a previously present stray backtick in `Day-2/knowledge_base.py`.
- If ChromaDB raises embedding-function compatibility errors, ensure the fallback embedding implements the interface required by the installed ChromaDB version. This project supplies a compatible fallback.
- Gemini generation requires `google.genai` and a valid `GEMINI_API_KEY`. Without them, the agent will still retrieve sources but will return a diagnostic text instead of an LLM answer.

Useful commands
---------------
Start streamlit and log to file (background):

```bash
nohup streamlit run Day-3/streamlit_app.py --server.port 8501 --server.address 127.0.0.1 > streamlit.log 2>&1 &
tail -f streamlit.log
```

Initialize git repo (optional):

```bash
git init
git add .
git commit -m "Initial commit - GDG RAG workshop" 
```

Testing
-------
- Unit tests (if present) can be run with `pytest`.
- The smoke tests in the workshop files (Day-1 / Day-2 / Day-3) can be executed manually with `python3` to validate each module.

Files of interest
-----------------
- `Day-1/text_cleaner.py`, `Day-1/semantic_similarity.py`, `Day-1/faq_finder.py`
- `Day-2/chunking_utility.py`, `Day-2/knowledge_base.py`
- `Day-3/gemini_wrapper.py`, `Day-3/rag_agent.py`, `Day-3/streamlit_app.py`

License
-------
This project is provided as-is for learning purposes. Adapt and reuse per your needs.

Contact / Next steps
--------------------
If you'd like, I can:
- Start the Streamlit server and watch logs while you use the UI
- Add a step-by-step local setup script for PyTorch + sentence-transformers
- Wire the Streamlit app to allow KB initialization without Gemini (so you can upload/fetch docs first)

Pick one and I'll implement it for you.