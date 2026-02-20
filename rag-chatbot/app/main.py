# app/main.py
import os
import shutil
import tempfile
import traceback
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# IMPORTANT: correct package path
from app.rag.ingest import ingest_file
from app.rag.chat import answer

load_dotenv()

app = FastAPI(title="RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only; lock down in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Only 'question' now (no model)
class ChatRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"status": "ok", "message": "RAG API is running. See /docs for Swagger UI."}

@app.post("/ingest")
async def ingest(upload: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(upload.filename)[1]) as tmp:
            shutil.copyfileobj(upload.file, tmp)
            tmp_path = tmp.name
        chunks = ingest_file(tmp_path)
        os.remove(tmp_path)
        return {"status": "ok", "chunks_indexed": chunks}
    except Exception as e:
        # 🔎 Print server-side stack for any hidden import calling OpenAI
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        response = answer(req.question)  # ✅ only question
        return {"answer": response}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

# (Optional) Plain LLM route to isolate OpenRouter vs. RAG
from langchain_openai import ChatOpenAI
@app.post("/chat_plain")
async def chat_plain(req: ChatRequest):
    try:
        llm = ChatOpenAI(
            model=os.getenv("OPENROUTER_MODEL"),
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            temperature=0,
        )
        text = llm.invoke(req.question)
        return {"answer": str(text)}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"chat_plain error: {e}")