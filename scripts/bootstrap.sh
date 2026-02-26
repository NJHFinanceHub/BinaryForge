#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

pushd frontend >/dev/null
npm install
popd >/dev/null

echo "Bootstrap complete. Run backend with: uvicorn app.main:app --app-dir backend --reload"
