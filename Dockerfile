FROM python:3.10.14-bullseye

WORKDIR /app

# System packages — libgles2/libgomp1 needed by MediaPipe + FAISS
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgles2 \
    libegl1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend code
COPY backend/ .

# Pre-download InsightFace buffalo_sc model weights (so first request is instant)
# This runs in the build layer — cached on re-builds
RUN python -c "\
from insightface.app import FaceAnalysis; \
app = FaceAnalysis(name='buffalo_sc', providers=['CPUExecutionProvider']); \
app.prepare(ctx_id=-1, det_size=(320,320)); \
print('InsightFace buffalo_sc model ready.')"

# Build celebrity face embedding database from Wikipedia photos
# This is the heavy step (~5-15 min first time, then Docker-cached)
RUN python build_celeb_embeddings.py

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
