#!/bin/bash

set -e

echo "Building TetriPy for WebAssembly..."

# Build the WASM version
python -m pygbag --build main.py

echo "Build complete! The game should now be available in the build/web directory."
