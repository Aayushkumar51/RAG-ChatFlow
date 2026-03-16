#!/usr/bin/env bash
# Ensure project root is on PYTHONPATH so "server" package is found (for Render)
set -e
cd "$(dirname "$0")"
export PYTHONPATH="${PYTHONPATH:+${PYTHONPATH}:}$(pwd)"
exec poetry run uvicorn main:app --host 0.0.0.0 --port "${PORT:-10000}"
