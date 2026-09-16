#!/usr/bin/env bash
# End-to-end self test: starts the local mock directory, scrapes it, stops it.
# Proves pagination, robots.txt enforcement, retries, extraction and dedup
# without touching a real site. Writes vendors.sample.csv.
set -euo pipefail
cd "$(dirname "$0")"
PORT="${PORT:-8099}"
PY="${PY:-.venv/bin/python}"

"$PY" tools/mock_site.py --port "$PORT" & MOCK_PID=$!
trap 'kill "$MOCK_PID" 2>/dev/null || true' EXIT
sleep 2

"$PY" scraper.py \
  --keyword "welding services" \
  --domain "127.0.0.1:${PORT}" \
  --max-pages 3 \
  --engine requests \
  --delay-min 0.05 --delay-max 0.1 \
  --search-url-template "http://{domain}/search?q={keyword}&page={page}" \
  --output vendors.sample.csv
