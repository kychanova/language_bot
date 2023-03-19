#!/bin/bash
docker compose down
git pull
echo "rebuild bot image"
docker compose build --no-cache
echo "up containers"
docker compose up -d