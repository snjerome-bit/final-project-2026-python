# Pong (But moded)

A small base implementation of Pong using Pygame.(But MODED)

Requirements
- Python 3.8+
- pygame (see `requirements.txt`)

Run

```bash
# create a virtualenv (recommended)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Controls
- W / S : move left paddle up/down
- Up / Down arrows : move right paddle
- R : reset scores and positions
- the blue balls give you power ups

Files
- `main.py` — main game loop and rendering
- `classes/paddle.py` — Paddle class
- `classes/ball.py` — Ball class

This is a minimal base you can extend (AI opponent, sounds, menu, polish).
