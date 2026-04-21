from uuid import uuid4

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import json
from pydantic import BaseModel, field_validator
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os





app=FastAPI()

sessions={}
Ollama_URL="http://localhost:11434/api/chat"
MODEL="mistral"


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/ui")
def ui():
    return FileResponse("static/index.html")

class ChatRequest(BaseModel):
    message: str
    system_prompt: str = "You are a helpful assistant"
    @field_validator("message")
    @classmethod
    def message_must_be_valid(cls, v):
        if not v.strip():
            raise ValueError("Message cannot be empty")
        if len(v) > 2000:
            raise ValueError("Message too long — max 2000 characters")
        return v.strip()



def call_ollama(message:str,stream:bool = False):
  try:
      response=requests.post(Ollama_URL,json={
          "model":MODEL,"messages":message,"stream":stream},
          stream=stream,timout=60)
      response.raise_for_status()
      return response
  except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Ollama is not running. Start it with: ollama serve")
  except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Ollama timed out. Try a shorter message.")
  except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}") 
          
      


@app.get("/")
def root():
    return{"status":"AI bacend is running"}

@app.get("/health")
def health():
    try:
        requests.get("http://localhost:11434/api/tags",timeout=3)
        return {"status":"ok","ollama":"reachable","model":MODEL}
    except:
        return {"status": "degraded", "ollama": "unreachable"}


@app.post("/chat/stream")
def chat(req: ChatRequest):
    messages=[
        {"role":"system","content":req.system_prompt},
        {"role":"user","content":req.message}]
    
    def generate():
       
        response = call_ollama(messages,stream=True)
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                token = chunk.get("message", {}).get("content", "")
                if token:
                    yield token

    return StreamingResponse(generate(), media_type="text/plain")




class ChatMemoryRequest(BaseModel):
    message: str 
    system_prompt: str=" You are a helpful assitant"
    session_id:str= ""

    @field_validator("message")
    @classmethod
    def message_must_be_valid(cls, v):
        if not v.strip():
            raise ValueError("Message cannot be empty")
        if len(v) > 2000:
            raise ValueError("Message too long — max 2000 characters")
        return v.strip()

@app.post("/chat/memory")
def chat_with_memory(req:ChatMemoryRequest):

    

    session_id=req.session_id or str(uuid4())

    if session_id not in sessions :
        sessions[session_id]=[]

    sessions[session_id].append({"role":"user","conten":req.message})

    messages = [{"role":"system", "content":req.system_prompt}]+ sessions[session_id]

    response= call_ollama(messages,stream=False)
    data=response.json()
    assistant_reply=data["message"]["content"]

    sessions[session_id].append({
        "role":"assistant",
        "content":assistant_reply
    })

    return {
        "response": assistant_reply,
        "session_id": session_id
    }


    
 
         

        
        
