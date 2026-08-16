#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="lc_dq_app"

docker rm -f "$CONTAINER_NAME"
