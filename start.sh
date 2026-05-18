#!/usr/bin/env bash
# start.sh — Launch CampusMind AI
set -e

PORT=${PORT:-8080}
UI_PATH="$(dirname "$0")/ui/streamlit_ui.py"

echo "Starting CampusMind AI on port $PORT..."

python -m streamlit run "$UI_PATH" \
  --server.port "$PORT" \
  --server.address 0.0.0.0 \
  --server.headless true \
  --browser.gatherUsageStats false
