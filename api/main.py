import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from common.db import Base, engine
from common import models
from api.routers import chat_router

# Create database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="OrderBot API")

# CORS — tighten allowed origins in production via env var if needed
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

# API routes
app.include_router(chat_router.router, prefix="/api/chat", tags=["Chat"])


@app.get("/api/health")
async def health():
    return {"status": "ok"}


# Serve React frontend (production build)
FRONTEND_DIR = Path(__file__).parent.parent / "frontend" / "dist"

if FRONTEND_DIR.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIR / "assets"), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        return FileResponse(FRONTEND_DIR / "index.html")