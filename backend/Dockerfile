FROM python:3.10-slim

WORKDIR /app

# All system libs MediaPipe needs on a headless Linux server
RUN apt-get update && apt-get install -y \
    libgl1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgles2 \
    libegl1 \
    libglvnd0 \
    libglx0 \
    libopengl0 \
    libgbm1 \
    libdrm2 \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

# Force software OpenGL rendering (no GPU on Render free tier)
ENV LIBGL_ALWAYS_SOFTWARE=1
ENV MESA_GL_VERSION_OVERRIDE=3.3

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
