# Amazon Pac-Man Game

A neon-styled, Amazon-branded Pac-Man clone built with Pygame. It is a Python-based reimagining of the classic Pac-Man arcade game featuring Amazon-themed visuals and branding. The game incorporates the iconic AMAZON letters in the maze design and uses the company's signature orange and blue color scheme.

This implementation features intelligent ghost AI with different behaviors, power pellets that temporarily make ghosts vulnerable, and a scoring system. The game includes modern enhancements like smooth animations, pixel-style wall effects, and customizable ghost behaviors while maintaining the core Pac-Man gameplay mechanics that made the original a classic.

![image alt](https://github.com/KareshmaAnanth/Amazon-Q/blob/51f17ff440e7ac1b69c55323a6191193563bb812/amazon-pacman/Pac%20man%20Game.png)

## Project Structure

amazon-pacman/

```bash

├── main.py          - Game entry point, main loop, and game state management

├── player.py        - Pac-Man player class with movement and animation logic

├── ghost.py         - Ghost AI implementation with different behaviors

├── maze.py          - Maze generation and rendering with AMAZON letters

├── utils.py         - Shared constants, utilities, and helper functions

├── test_game.py     - Unit tests for game components

└── README.md        - Project documentation
```

## Installation

1. Make sure you have Python 3.x installed on your system.
2. Install the required dependencies:
   ```bash
   pip install pygame
   ```

## How to Play

1. Run the game:
   ```bash
   python main.py
   ```

2. Controls:
   - **Arrow keys**: Move Pac-Man
   - **P**: Pause/Resume game
   - **R**: Restart game (when game over)
   - **ESC**: Access menu/Quit game
   - **Enter**: Start game from/Continue after death

## Features

- Amazon-themed maze layout spelling "AMAZON Q CLI"
- Neon-style dark theme with glowing effects
- On-screen display showing score and remaining lives
- "Amazon Arcade" intro screen
- Grid-based movement for the player-controlled Pac-Man character using arrow keys
- Classic Pac-Man gameplay mechanics
- Collision detection between Pac-Man, ghosts, and walls
- Three ghost enemies with unique behaviors (random, chase, scatter)
- Pellet and power pellet collection mechanics with score increments
- Three lives system with Game Over logic
- Pause (P) and restart (R) functionality

## Game Mechanics

### Pac-Man
- Moves through the maze collecting pellets
- Gains points for each pellet collected
- Power pellets allow Pac-Man to eat ghosts temporarily
- Has 3 lives; loses a life when touched by a ghost (unless powered up)


### Ghosts
- Four ghosts with different behaviors:
  - Red: Chase mode - directly pursues Pac-Man
  - Pink: Scatter mode - targets a position ahead of Pac-Man
  - Cyan: Random movement
  - Orange: Random movement
- Ghosts turn blue and can be eaten when Pac-Man collects a power pellet
- Eaten ghosts return to their starting position

### Scoring
- Regular pellet: 10 points
- Power pellet: 50 points
- Ghost: 200 points

## Customization

You can customize the game by modifying the constants in `utils.py`, such as colors, speeds, and game settings.


### More Detailed Examples
1. Ghost Behaviors:
```python
# Different ghost behaviors can be observed:
- Red ghost: Direct chase
- Pink ghost: Ambush ahead of player
- Cyan/Orange ghosts: Random movement
```

2. Power Pellet Usage:
```python
# Collect power pellets to:
- Make ghosts vulnerable (blue)
- Earn bonus points for eating ghosts
- Temporary ghost state lasts 6 seconds
```

## Component Interactions:
1. Main game loop manages state transitions and timing
2. Player movement responds to keyboard input and maze boundaries
3. Ghost AI calculates paths based on player position and behavior type
4. Collision detection handles pellet collection and ghost interactions
5. Maze renderer draws walls, pellets, and power-ups
6. Score system tracks points and remaining lives
7. Animation system handles player and ghost movements

## Data Flow
The game follows a classic arcade game loop architecture with state management and component interaction.

```ascii
[Input] -> [Game State] -> [Update Logic] -> [Collision Detection] -> [Render]
   ^                            |                     |                  |
   |                           v                     v                  v
[Player Input] <- [Ghost AI] <- [Movement] <- [Score/Lives] <- [Display]
```

## Credits

Created as an Amazon-themed Pac-Man clone for demonstration purposes.
Created with Python and Pygame with help of Amazon Q Cli

---

Enjoy the game!
