############################
# Stage 1: Build Frontend
############################
FROM node:18-alpine AS frontend-builder

WORKDIR /frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./

# Build frontend
RUN npm run build

# Debug (shows build output folder in logs)
RUN ls -la


############################
# Stage 2: Backend Runtime
############################
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend
COPY api ./api
COPY common ./common

# 🔥 COPY THE CORRECT FRONTEND OUTPUT
# If CRA → build
# If Vite → dist
COPY --from=frontend-builder /frontend/build ./frontend/build
COPY --from=frontend-builder /frontend/dist ./frontend/build

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
