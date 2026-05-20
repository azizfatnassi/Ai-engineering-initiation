# AI Engineer Journey — Phase 1 Projects

> Everything runs locally. No paid APIs. Ollama + Mistral 7B.

---

## 📄 RAG App — `rag_app/`

Upload a PDF or text file, ask questions about it, get streamed answers with source references.

### Features
- PDF + TXT ingestion and chunking (LangChain + pypdf)
- ChromaDB vector store for semantic search
- Ollama Mistral 7B — fully local
- `/upload` — ingest a document
- `/ask` — single response with sources
- `/ask-stream` — streaming response token by token
- Angular 17 frontend — chat unlocks after upload
- Full error handling: empty vectorstore guard, Ollama down guard

### Run the backend
```bash
cd rag_app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Run the frontend
```bash
cd rag-frontend
npm install
ng serve
```

Open `http://localhost:4200`

> Requires Ollama running with Mistral:
> ```bash
> ollama pull mistral
> ollama serve
> ```

---

## 🔍 Code Search — `code_search/`

Search your Python codebase by meaning, not keywords.  
Type *"stream tokens to client"* → finds `ask_stream_endpoint` instantly.

### Features
- AST-based function parser — chunks by function boundary, not character count
- Handles both regular and async functions
- Local embeddings via `sentence-transformers` (`all-MiniLM-L6-v2`) — no API needed
- ChromaDB vector storage with function name, file path, line number metadata
- `/search` — semantic search endpoint
- `/index` — re-index any directory on demand
- Dark theme HTML frontend with scored result cards

### Run
```bash
cd code_search
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn chromadb sentence-transformers

# Index your codebase
python indexer.py

# Start the API
uvicorn main:app --reload

# Open the frontend
start index.html
```

Swagger UI at `http://localhost:8000/docs`

---

*Built by [@azizfatnassi](https://github.com/azizfatnassi)*
