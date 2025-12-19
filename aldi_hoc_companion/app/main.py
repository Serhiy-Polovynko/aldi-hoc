from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from aldi_hoc_companion.agent import ask
from aldi_hoc_companion.models import ChatRequest, ChatResponse, TokenUsageResponse
from aldi_hoc_companion.core.config import get_settings

app = FastAPI(title="Aldi HoC Companion")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest):
    try:
        response = await ask(body.question)
        return ChatResponse(
            answer=response.result.answer,
            sql_used=response.result.sql_used,
            row_count=response.result.row_count,
            usage=TokenUsageResponse(
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
                total_tokens=response.usage.total_tokens,
                input_cost_usd=response.usage.input_cost_usd,
                output_cost_usd=response.usage.output_cost_usd,
                total_cost_usd=response.usage.total_cost_usd,
                model=response.usage.model,
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    settings = get_settings()
    return {"status": "ok", "model": settings.openai_model}


STATIC_DIR = Path(__file__).parent / "static"


@app.get("/")
async def serve_frontend():
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
