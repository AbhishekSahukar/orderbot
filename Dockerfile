# ---------- Frontend build ----------
FROM node:18-alpine AS frontend-builder
WORKDIR /frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .
RUN npm run build   # produces /frontend/dist

# ---------- Backend + Nginx ----------
FROM python:3.10-slim
WORKDIR /app

# Install nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Copy backend
COPY backend/ ./backend
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy React DIST 
COPY --from=frontend-builder /frontend/dist /usr/share/nginx/html

# Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD service nginx start && uvicorn backend.api.main:app --host 0.0.0.0 --port 8000
