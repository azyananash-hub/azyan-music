#!/usr/bin/env bash
# Jalankan website ARCHER secara lokal: pasang dependensi bila perlu, build, lalu serve.
# Pemakaian: ./scripts/run-site.sh [port]   (default 4173)
set -euo pipefail
cd "$(dirname "$0")/.."
PORT="${1:-4173}"

if [ ! -d node_modules ]; then
  npm ci
fi
npm run build
exec npx vite preview --port "$PORT" --strictPort --host
