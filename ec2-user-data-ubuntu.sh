#!/bin/bash
set -e

apt-get update
apt-get install -y docker.io
systemctl enable --now docker

docker pull DOCKERHUB_USERNAME/plant-tracker:1.0
docker volume create plant-data
docker run -d \
  --name plant-tracker \
  --restart unless-stopped \
  -p 2468:80 \
  -v plant-data:/data \
  DOCKERHUB_USERNAME/plant-tracker:1.0
