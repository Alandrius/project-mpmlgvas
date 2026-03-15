#!/usr/bin/env bash

set -e

echo "Starting build..."

# Go to script directory (project root)
cd "$(dirname "$0")"

# Choose python command
if command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD="python"
else
  echo "Error: Python is not installed."
  exit 1
fi

echo "Using: $PYTHON_CMD"

echo "Installing PyInstaller..."
"$PYTHON_CMD" -m pip install pyinstaller

echo "Installing app dependencies (tabulate, colorama) so they are bundled..."
"$PYTHON_CMD" -m pip install tabulate colorama

echo "Cleaning old build folders..."
rm -rf build dist assistant.spec

echo "Building executable..."
"$PYTHON_CMD" -m PyInstaller --onefile --name assistant assistant.py

echo "Done."
echo "Executable file: dist/assistant"
