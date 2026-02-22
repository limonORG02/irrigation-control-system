#!/usr/bin/env bash
set -e

echo "Checking for Python3..."
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python3 is required. Install Python 3 and rerun." >&2
  exit 1
fi

PY=python3

echo "Creating virtual environment .venv..."
$PY -m venv .venv

echo "Activating virtual environment and installing requirements..."
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "Initializing database and running demo start..."
python start.py

echo "Installation complete."
