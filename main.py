from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from db_agent import process_question


app = FastAPI(
    title="Employee AI Assistant",
    description="AI-powered employee support and analytics API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def root():
    return {
        "message": "Employee AI Assistant API is running"
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    response = process_question(request.message)

    return {
        "response": response
    }