import os
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from app.agent import chat_with_agent

# Cargar variables de entorno
load_dotenv()

# Configurar la aplicación FastAPI
app = FastAPI(
    title="Agente de Optimización de Tráfico",
    description="API para el agente de optimización de tráfico urbano",
    version="1.0.0"
)

# Configurar CORS
origins = [
    "http://localhost:5173",  # Origen de desarrollo de Vite
    "http://localhost:3000",
    "http://localhost:8000",
    "*",  # Permitir cualquier origen en desarrollo
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de datos
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

# Endpoints
@app.get("/")
async def root():
    return {"message": "Bienvenido al API del Agente de Optimización de Tráfico"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Procesa un mensaje del usuario y devuelve la respuesta del agente.
    
    - **message**: El mensaje del usuario
    - **session_id**: Identificador opcional de sesión para mantener conversaciones separadas
    """
    try:
        # Usar el session_id proporcionado o generar uno nuevo
        session_id = request.session_id or "default"
        
        # Procesar el mensaje con el agente
        output = chat_with_agent(request.message, session_id)
        
        return {"response": output, "session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el mensaje: {str(e)}")

@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado del servicio"""
    return {"status": "ok"}

# Configuración para ejecutar la aplicación
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
