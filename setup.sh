#!/bin/bash
# ═══════════════════════════════════════════════════════════
# setup.sh — Face Analyzer EC2 Setup Script
# Ubuntu 22.04 LTS | Run as: bash setup.sh YOUR_EC2_IP
# ═══════════════════════════════════════════════════════════

set -e
EC2_IP=${1:-"localhost"}

echo "══════════════════════════════════════"
echo " Face Analyzer — EC2 Setup"
echo " EC2 IP: $EC2_IP"
echo "══════════════════════════════════════"

# ── System update ──────────────────────────────────────────
echo "[1/8] Updating system packages..."
sudo apt-get update -y && sudo apt-get upgrade -y

# ── Python 3.10 ────────────────────────────────────────────
echo "[2/8] Installing Python 3.10..."
sudo apt-get install -y python3.10 python3.10-venv python3-pip

# ── Node.js 20 ─────────────────────────────────────────────
echo "[3/8] Installing Node.js 20..."
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# ── Docker ─────────────────────────────────────────────────
echo "[4/8] Installing Docker..."
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker

# ── Swap file (critical for t2.micro) ─────────────────────
echo "[5/8] Creating 2 GB swap file..."
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
echo "Swap enabled:"
free -h

# ── Clone project ──────────────────────────────────────────
echo "[6/8] Cloning project..."
# If you have a git repo, replace this with: git clone YOUR_REPO_URL face-analyzer
# Otherwise copy files manually to ~/face-analyzer
if [ ! -d "$HOME/face-analyzer" ]; then
  echo "  → Please copy your face-analyzer folder to $HOME/face-analyzer"
  echo "    or run: git clone YOUR_REPO_URL $HOME/face-analyzer"
fi

# ── Update CORS for EC2 IP ─────────────────────────────────
echo "[7/8] Configuring EC2 IP: $EC2_IP ..."
if [ -f "$HOME/face-analyzer/docker-compose.yml" ]; then
  sed -i "s|http://localhost:3000|http://$EC2_IP:3000|g" \
    "$HOME/face-analyzer/docker-compose.yml"
  sed -i "s|http://localhost:8000|http://$EC2_IP:8000|g" \
    "$HOME/face-analyzer/docker-compose.yml"
fi

# ── Launch ─────────────────────────────────────────────────
echo "[8/8] Starting docker-compose..."
if [ -d "$HOME/face-analyzer" ]; then
  cd "$HOME/face-analyzer"
  docker compose up -d --build
  echo ""
  echo "══════════════════════════════════════"
  echo " ✅ App running!"
  echo " Frontend : http://$EC2_IP:3000"
  echo " Backend  : http://$EC2_IP:8000"
  echo " Health   : http://$EC2_IP:8000/health"
  echo "══════════════════════════════════════"
else
  echo "⚠ $HOME/face-analyzer not found. Copy project files first, then run:"
  echo "  cd ~/face-analyzer && docker compose up -d --build"
fi
