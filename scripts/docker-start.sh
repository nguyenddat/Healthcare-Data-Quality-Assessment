#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="lc-dq-app"
CONTAINER_NAME="lc_dq_app"

docker build -t "$IMAGE_NAME" .
docker run -d --name "$CONTAINER_NAME" -p 8000:8000 --env-file .env "$IMAGE_NAME"
