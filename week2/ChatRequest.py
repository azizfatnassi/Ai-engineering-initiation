
from pydantic import BaseModel, field_validator

class ChatRequest(BaseModel):
    message:str
    system_prompt:str="You are a helpful assitant."
    
    @field_validator("message")
    @classmethod
    def message_must_not_be_empty(cls,v):
        if not v.strip():
            raise ValueError ( "Message cannot be empty")
        if len(v)> 1000:
            raise ValueError("Message too long- max 1000 characters")
        return v  