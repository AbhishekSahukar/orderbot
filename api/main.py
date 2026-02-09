from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from common.db import Base, engine
from common import models
from api.routers import chat_router

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Status Chatbot API")

# ✅ Allow frontend (React) to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(chat_router.router, prefix="/api/chat", tags=["Chat"])

# -----------------------------
# ✅ React frontend (SAFE ADDON)
# -----------------------------
if os.path.exists("frontend/dist"):
    app.mount(
        "/static",
        StaticFiles(directory="frontend/dist/assets"),
        name="static",
    )

    @app.get("/", include_in_schema=False)
    async def serve_react():
        return FileResponse("frontend/dist/index.html")
else:
    # 🔒 Original behavior preserved
    @app.get("/")
    async def root():
        return {"message": "Order Status Chatbot API is running 🚀"}
