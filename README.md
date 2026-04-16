# SUPER PONG

An advanced Pong game built with Pygame featuring fire sprites, power-ups, special abilities, shields, and dynamic visual effects.

## Features

- **Fire Ball Sprite**: Animated fireball that rotates based on movement direction
- **Dual Ability System**: Each player can activate special abilities by filling their meter
  - **Ghost Mode**: Make the ball pass through paddles (semi-transparent)
  - **Double Hit**: Hit the ball at 2x speed
- **Power-up System**:
  - **Speed Boosts**: Temporarily increase paddle speed (spawns every 30 seconds)
  - **Shield Blocks**: Block incoming points with magical shields (spawns every 60 seconds)
- **Visual Effects**:
  - Doctor Strange-style portal animation when shields activate
  - Particle effects for double-hit and shield blocks
  - Screen shake on special events
  - Glowing meter displays
- **Win Condition**: First player to 10 points wins
- **Responsive Controls**: WASD and Arrow keys for smooth paddle movement

## Requirements

- Python 3.8+
- pygame (see `requirements.txt`)

## Run

```bash
# create a virtualenv (recommended)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Controls

### Movement
- **W / S** : move left paddle (White) up/down
- **Up / Down arrows** : move right paddle (Yellow) up/down

### White Paddle (Left Side)
- **Capslock** : Activate Ghost Mode (requires 1.0 meter)
- **Left Shift** : Activate Super Hit (requires 2.0 meter)
- **Q** : Parry - cancel ghost mode when near ball

### Yellow Paddle (Right Side)
- **Return** : Activate Ghost Mode (requires 1.0 meter)
- **Right Shift** : Activate Super Hit (requires 2.0 meter)
- **/** : Parry - cancel ghost mode when near ball

### Game
- **Left Click** : Start game or restart after win
- **Quit Button** : Exit game

## Game Mechanics

### Meter System
- Meters fill when you hit the ball with your paddle (+0.25 per hit)
- **Blue meter** (bottom): First ability level (0.0-1.0)
- **Red meter** (bottom): Second ability level (1.0-2.0)
- Meter resets when you get scored on

### Abilities
- **Ghost Mode**: Ball becomes semi-transparent and passes through paddles for 1 second
- **Double Hit**: Ball bounces at 2x speed and creates particle effects
- **Parry**: Quickly cancel an incoming ghost ball to make it solid again

### Shields
- Shields appear as blue powerup balls on the screen
- Collect them to gain immunity to one incoming point
- When a shot is blocked: Portal effect spins, particles scatter, ball bounces back
- Shield count displays with magical spinning animation

### Speed Boosts
- Speed boosts appear as blue powerup balls on the screen
- Collect them to gain 10 seconds of 2x paddle speed
- Speed timer displays and counts down

## Files

- `main.py` — main game loop, rendering, and game state management
- `classes/paddle.py` — Paddle class with movement and ability tracking
- `classes/ball.py` — Ball class with physics, ghost mode, and fire sprite
- `classes/powerup_ball.py` — PowerupBall class for shields and speed boosts
- `classes/particles.py` — ParticleManager for visual effects
- `PNG/fire.png` — Fire sprite asset for the ball

## Game Over

When a player reaches 10 points:
- Win message displays
- Restart button appears to play again
- Quit button to exit the game
