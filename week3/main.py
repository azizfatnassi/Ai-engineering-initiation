
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, field_validator
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from uuid import uuid4
import aiofiles


app= FastAPI()
llm = ChatOllama(model="mistral", base_url="http://localhost:11434")

prompt= ChatPromptTemplate.from_messages(
    [("system","{system_prompt}"),
     MessagesPlaceholder("history"),
     ("human","{question}")])

chain= prompt | llm | StrOutputParser()

sessions={}

class ChatRequest(BaseModel):
    message:str
    session_id:str=""
    system_prompt:str="you are a helpful assitant"
    @field_validator("message")
    @classmethod
    def message_must_be_valid(cls,v):
        if not v.strip():
            raise ValueError("Message cannot be empty")
        if len(v) > 2000:
            raise ValueError("Message too long — max 2000 characters")
        return v.strip()
    

@app.get("/")
def root():
    return {"status":"Week 3 Langchain backend running"}
@app.get("/health")
def health():
    try:
        llm.invoke([HumanMessage(content="ping")])
        return {"status":"ok","ollama":"reachable"}
    except :
        return {"status":"degraded", "ollama": "unreachable"}
    
@app.post("/chat")
def chat(req:ChatRequest):
    session_id=req.session_id or str(uuid4())
    if session_id not in sessions:
        sessions[session_id]=[]

    try: 
            response= chain.invoke ({
                "system_prompt": req.system_prompt,
                "history":sessions[session_id],
                "question": req.message

            })
    except Exception as e:
     raise HTTPException(status_code=503, detail=str(e))

    sessions[session_id].append(HumanMessage(content=req.message))
    sessions[session_id].append(AIMessage(content=response))
    return {"response": response, "session_id": session_id}


@app.post("/chat/stream")
def chat_stream(req:ChatRequest):
     session_id=req.session_id or str(uuid4())

     if session_id not in sessions :
      sessions[session_id]=[]
      history_snapshot= list(sessions[session_id])
     def generate():
        full_response=""
        try:
          for chunk in chain.stream({
                "system_prompt": req.system_prompt,
                "history": history_snapshot,
                "question": req.message
            }):

           full_response+=chunk
           yield chunk 
        except  Exception:
          yield "Error:Ollama is not reachable"
        
        sessions[session_id].append(HumanMessage(content=req.message))
        sessions[session_id].append(AIMessage(content=full_response))

     return StreamingResponse(generate(),media_type="text/plain")
        

     

         