# ── Stage 1: build the React frontend ─────────────────────────────────────────
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build


# ── Stage 2: Python backend + serve built frontend ─────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Backend source
COPY api/      ./api/
COPY common/   ./common/
COPY seed_data.py ./

# React build output from stage 1
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

EXPOSE 8000

# Seed DB on first run (idempotent), then start the server
CMD ["sh", "-c", "python seed_data.py && uvicorn api.main:app --host 0.0.0.0 --port 8000"]