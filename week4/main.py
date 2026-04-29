

import chromadb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from sentence_transformers import SentenceTransformer
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, collection 
    print("loading embedding model .. ")
    model=SentenceTransformer("all-MiniLM-L6-v2")
    client= chromadb.PersistentClient(path="./chromadb")
    collection= client.get_or_create_collection(name="knowledge_base")
    print(f"ChromaDB ready — {collection.count()} documents loaded")
    yield


app= FastAPI(lifespan=lifespan)

class AddDocumentRequest(BaseModel):
    documents: list[str]
    topic: str= "general"

    @field_validator("documents")
    @classmethod
    def documents_must_not_be_empty(cls, v):
     if not v:
        raise ValueError("Documents list cannot be empty")
     return v
        
class SearchRequest(BaseModel):
    query: str 
    n_results: int=3
    topic:str=""

    @field_validator("query")
    @classmethod
    def query_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()


@app.get("/")
def root():
    return {"status": "Semantic search API running","documents":collection.count()}


@app.post("/documents/add")
def add_doc(req:AddDocumentRequest):
    embeddings=model.encode(req.documents)
    count=collection.count()
    ids= [f"doc_{count + i}" for i in range(len(req.documents))]
    metadatas= [{"topic": req.topic,"chunk": i+ 1} for i in range(len(req.documents))]

    collection.add(
        embeddings= embeddings,
        documents= req.documents,
        metadatas= metadatas,
        ids=ids
    )
    return{"added":len (req.documents), "total": collection.count()}

@app.post("/search")
def search(req: SearchRequest):
    if collection.count() == 0:
        raise   HTTPException(status_code=400,detail="No documentsin the database")

    query_embedding= model.encode(req.query).tolist()

    query_params={
        "query_embeddings": [query_embedding],
        "n_results": min(req.n_results,collection.count())
    }

    if req.topic: 
     query_params["where"]={"topic" :req.topic}
    try:
      results= collection.query(**query_params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
         "query": req.query,
         "results" : [
             {
                 "text": results["documents"][0][i],
                 "topic":results["metadatas"][0][i]["topic"],
                 "distance": round(results["distances"][0][i],3)
             }

             for i in range(len(results["documents"][0]))
         ]

        }

@app.delete("/documents/clear")
def clear_documents():
    client = chromadb.PersistentClient(path="./chroma_db")
    client.delete_collection("knowledge_base")
    client.get_or_create_collection("knowledge_base")
    return {"status": "Collection cleared"}

 
