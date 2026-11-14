#!/bin/sh
# Start edge server (plain HTTP on private LAN; iOS app allows local networking).
# Works on Mac (dev) and UNO Q (Linux).
cd "$(dirname "$0")" || exit 1
IP=$(ipconfig getifaddr en0 2>/dev/null || hostname -I | awk '{print $1}')
echo "Server: http://$IP:8000"
exec .venv/bin/uvicorn edge.server:app --host 0.0.0.0 --port 8000 --reload --reload-dir edge --timeout-graceful-shutdown 1
