

from fastapi import FastAPI
from pydantic import BaseModel

from app.rag import ask


app = FastAPI()

class QuestionRequest(BaseModel):
 
 question: str

@app.post("/ask")
def ask_question(request: QuestionRequest):
 answer= ask(request.question)
 return {"question": request.question, "answer":answer}

@app.get("/health")
def health():
    return {"status": "ok"}
