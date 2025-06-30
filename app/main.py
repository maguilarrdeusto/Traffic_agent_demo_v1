import os
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from app.agent import chat_with_agent

# Load environment variables
load_dotenv()

# Configure FastAPI application
app = FastAPI(
    title="Agente de Optimización - Deusto",
    description="API para el agente de optimización de tráfico de Deusto",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:5173",  # Vite development origin
    "http://localhost:3000",
    "http://localhost:8000",
    "*",  # Allow any origin in development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

# Endpoints
@app.get("/")
async def root():
    return {"message": "Bienvenido al API del Agente de Optimización de Deusto"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a user message and return the agent's response.
    
    - **message**: The user's message
    - **session_id**: Optional session identifier to maintain separate conversations
    """
    try:
        # Use the provided session_id or generate a new one
        session_id = request.session_id or "default"
        
        # Process the message with the agent
        output = chat_with_agent(request.message, session_id)
        
        return {"response": output, "session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.get("/health")
async def health_check():
    """Endpoint to check the service status"""
    return {"status": "ok", "service": "Agente de Optimización - Deusto"}

# Configuration to run the application
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)

