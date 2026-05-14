import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from common.db import Base, engine
from common import models
from api.routers import chat_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="OrderBot API")

# CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(
    chat_router.router,
    prefix="/api/chat",
    tags=["Chat"],
)


# Health check
@app.get("/api/health")
async def health():
    return {"status": "ok"}


# Frontend build directory
FRONTEND_DIR = Path(__file__).parent.parent / "frontend" / "dist"

if FRONTEND_DIR.exists():

    # Serve Vite assets
    assets_dir = FRONTEND_DIR / "assets"

    if assets_dir.exists():
        app.mount(
            "/assets",
            StaticFiles(directory=assets_dir),
            name="assets",
        )

    # Optional favicon
    favicon_path = FRONTEND_DIR / "favicon.ico"

    if favicon_path.exists():

        @app.get("/favicon.ico", include_in_schema=False)
        async def favicon():
            return FileResponse(favicon_path)

    # Serve root frontend
    @app.get("/", include_in_schema=False)
    async def serve_root():
        return FileResponse(FRONTEND_DIR / "index.html")

    # React Router support
    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):

        requested_path = FRONTEND_DIR / full_path

        # Serve actual existing files
        if requested_path.exists() and requested_path.is_file():
            return FileResponse(requested_path)

        # Otherwise fallback to React app
        return FileResponse(FRONTEND_DIR / "index.html")