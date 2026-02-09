# -----------------------
# Frontend build stage
# -----------------------
FROM node:18-alpine AS frontend-builder

WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build   # produces /frontend/dist


# -----------------------
# Backend + Nginx stage
# -----------------------
FROM python:3.10-slim

# Install nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Set working dir
WORKDIR /app

# Copy backend (ROOT files, not backend/)
COPY . .

# Copy built frontend
COPY --from=frontend-builder /frontend/dist ./frontend/dist

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Expose EB port
EXPOSE 8000

# Start both nginx + uvicorn
CMD service nginx start && uvicorn api.main:app --host 0.0.0.0 --port 8000
