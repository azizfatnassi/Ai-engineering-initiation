from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from search import search_code as find_code

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    query: str
    n_results: int = 3

class SearchResult(BaseModel):
    function_name: str
    file_path: str
    line_number: int
    score: float
    code: str

@app.get("/")
def root():
    return {"status": "code search API is running"}

@app.post("/search", response_model=list[SearchResult])
def search(request: SearchRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    return find_code(request.query, request.n_results)

@app.post("/index")
def index(directory: str = '../rag_app'):
    from indexer import index_codebase
    index_codebase(directory)
    return {"status": "indexed successfully"}