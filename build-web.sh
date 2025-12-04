#!/bin/bash

# Build script for TetriPy WASM using pygbag

echo "Building TetriPy for WebAssembly..."

# Activate virtual environment if it exists
if [ -d "tetripy-venv" ]; then
    source tetripy-venv/bin/activate
fi

# Install dependencies if not already installed
pip install -r requirements.txt

# Build the WASM version
python -m pygbag --build main.py

echo "Build complete! The game should now be available in the build/web directory."

