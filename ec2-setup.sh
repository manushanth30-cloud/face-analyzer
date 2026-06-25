#!/bin/bash
set -e

echo "=== Face Analyzer Backend Setup (Docker) ==="

# Install Docker
sudo apt-get update -y
sudo apt-get install -y docker.io git
sudo systemctl start docker
sudo systemctl enable docker

# Clone the repo
cd /home/ubuntu
if [ -d "face-analyzer" ]; then
    echo "Repo exists, pulling latest..."
    cd face-analyzer && git pull origin main
else
    git clone https://github.com/manushanth30-cloud/face-analyzer.git
    cd face-analyzer
fi

# Build Docker image (fresh, no cache)
echo "=== Building Docker image (this takes ~5 mins)... ==="
sudo docker build --no-cache -t face-analyzer-backend .

# Stop old container if exists
sudo docker rm -f face-analyzer-backend 2>/dev/null || true

# Run container with auto-restart
sudo docker run -d \
    --name face-analyzer-backend \
    --restart always \
    -p 8000:8000 \
    face-analyzer-backend

sleep 3
echo ""
echo "=== Setup Complete! ==="
sudo docker ps | grep face-analyzer
echo ""
echo "Backend running at: http://13.232.72.80:8000"
echo "View logs: sudo docker logs -f face-analyzer-backend"
