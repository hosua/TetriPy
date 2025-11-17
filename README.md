# TetriPy

An implementation of Tetris in Python

https://github.com/hosua/TetriPy/assets/22788738/100064d8-b6e3-45bc-9781-021b4dcaf954

If you would like to start the game on a higher level, run the game with the
starting level as the argument. e.g. `python3 main.py 30`.

# Controls

`left/right arrow keys` to move the piece.

`z/x keys` to rotate the piece left/right respectively.

`c` hold the piece.

`p` to pause the game.

`space` hard drop the piece.

`esc` to quit the game at any time.

# Requirements

Requires `Python 3.10+` and pygame 2.6.0+ (for Python 3.13 compatibility).

# Installation

TetriPy requires pygame and Python 3.10+. 

**Note:** If you're using Python 3.13, you'll need pygame 2.6.0 or later (which is already specified in requirements.txt).

1. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv tetripy-venv
   source tetripy-venv/bin/activate  # On Windows: tetripy-venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the game:
   ```bash
   python main.py
   ```

# WebAssembly Build

TetriPy can be built for WebAssembly using pygbag, allowing it to run in web browsers.

## Building for WebAssembly

1. Activate your virtual environment (if using one):
   ```bash
   source tetripy-venv/bin/activate  # On Windows: tetripy-venv\Scripts\activate
   ```

2. Install dependencies (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

3. Build the WASM version:
   ```bash
   ./build_wasm.sh
   ```
   
   Or manually:
   ```bash
   python -m pygbag main.py
   ```

4. The build output will be in the `build/web` directory. You can serve it using any static web server:
   ```bash
   cd build/web
   python -m http.server 8000
   ```
   
   Then open `http://localhost:8000` in your browser.

## Running Locally (Desktop)

For desktop use, simply run:
```bash
python main.py
```

