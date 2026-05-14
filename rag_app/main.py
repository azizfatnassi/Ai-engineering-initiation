

from contextlib import asynccontextmanager
import os
import shutil
from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.rag import ask,ask_stream, load_llm, load_vectorstore
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse

from app.ingest import ingest_documents



resources = {}
UPLOAD_DIR="./data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@asynccontextmanager
async def lifespan( app : FastAPI):
  print("loading vectorstore and LLM ...")
  try:
        resources["llm"] = load_llm()
        print("✅ LLM loaded")
  except Exception as e:
        print(f"⚠️  WARNING: Could not load LLM: {e}")
        resources["llm"] = None

  print("Loading vectorstore...")
  try:
        resources["vectorstore"] = load_vectorstore()
        count = resources["vectorstore"]._collection.count()
        if count == 0:
            print("⚠️  Vectorstore is empty — waiting for first upload")
        else:
            print(f"✅ Vectorstore loaded with {count} chunks")
  except Exception as e:
        print(f"⚠️  Could not load vectorstore: {e}")
        resources["vectorstore"] = None

  yield
  resources.clear()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

class QuestionRequest(BaseModel):
 
 question: str

class SourceChunk(BaseModel):
  content: str
  source: str
  page: Optional[int]= None 
  

class QuestionResponse(BaseModel):
  question: str
  answer: str
  sources:list[SourceChunk]


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # 1. Validate file type
    allowed_extensions = [".pdf", ".txt"]
    ext = os.path.splitext(file.filename)[-1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{ext}' not supported. Use PDF or TXT."
        )

    # 2. Save file to disk
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"✅ Saved file: {file_path}")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {str(e)}"
        )

    # 3. Ingest into vectorstore
    try:
        ingest_documents(file_path)
        resources["vectorstore"] = load_vectorstore()
        return {
            "message": f"File '{file.filename}' uploaded and indexed successfully.",
            "file": file.filename
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"File saved but indexing failed: {str(e)}"
        )

  

@app.post("/ask",response_model= QuestionResponse)
def ask_question(request: QuestionRequest):
 if resources['vectorstore'] is  None:
    raise HTTPException(status_code=400,
                        detail="no documents uploaded yet.")
 try:
  result= ask(
    question= request.question,
    vectorstore=resources["vectorstore"],
    llm=resources["llm"]
  )
  return QuestionResponse(
    question=request.question,
    answer= result["answer"],
    sources= result["sources"]
 )

 except Exception as e:
  raise HTTPException(status_code=503, detail=f"LLM error. Is Ollama running? Detail: {str(e)}")



@app.post("/ask-stream")
def ask_stream_endpoint(request: QuestionRequest):
  if resources['vectorstore'] is  None:
    raise HTTPException(status_code=400,
                        detail="no documents uploaded yet.") 
  def generate():
      try:
        for token in ask_stream(
            question=request.question,
            vectorstore=resources["vectorstore"],
            llm=resources["llm"]
        ):
            yield token
      except  Exception as e:
            yield f"\n\n[Error: LLM unreachable. Is Ollama running? {str(e)}]"

  return StreamingResponse(generate(), media_type="text/plain")






@app.get("/")
def root():
    return FileResponse("static/index.html")
