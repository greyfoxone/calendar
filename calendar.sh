#!/bin/sh
set -e

cd "$(dirname "$0")"
PYTHON=python3
VENV=".venv"

if [ ! -d "$VENV" ]; then
  $PYTHON -m venv "$VENV"
  . "$VENV/bin/activate"
  pip install --upgrade pip
  pip install -r requirements.txt
else
  . "$VENV/bin/activate"
fi

"$VENV/bin/python" "$(realpath "$0").py"