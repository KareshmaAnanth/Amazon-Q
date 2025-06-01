"""
Utility functions and constants for the Amazon Pac-Man game.
"""
import pygame
import os

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
NEON_BLUE = (0, 155, 255)  # Amazon blue
NEON_YELLOW = (255, 153, 0)  # Amazon orange

# Game settings
TILE_SIZE = 19  # Adjusted tile size for extended maze
PLAYER_SPEED = 3  # Slightly slower for better control
GHOST_SPEED = 2
SCREEN_WIDTH = 1080  # Width for extended maze
SCREEN_HEIGHT = 700  # Height for maze
FPS = 60

# Scoring
PELLET_POINTS = 10
POWER_PELLET_POINTS = 50
GHOST_POINTS = 200

# Game states
STATE_INTRO = 0
STATE_PLAYING = 1
STATE_PAUSED = 2
STATE_GAME_OVER = 3
STATE_PLAYER_DEAD = 4  # New state for player death animation

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Asset paths
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")

def load_image(name):
    """Load an image from the assets directory."""
    try:
        return pygame.image.load(os.path.join(ASSET_DIR, name))
    except pygame.error:
        print(f"Couldn't load image: {name}")
        return pygame.Surface((TILE_SIZE, TILE_SIZE))

def load_sound(name):
    """Load a sound from the assets directory."""
    try:
        return pygame.mixer.Sound(os.path.join(ASSET_DIR, name))
    except pygame.error:
        print(f"Couldn't load sound: {name}")
        return None

def draw_text(surface, text, size, x, y, color=WHITE):
    """Draw text on the given surface."""
    # Use the default pygame font
    font = pygame.font.Font(None, size)
    
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def create_neon_surface(width, height, color, intensity=10):
    """Create a surface with a neon glow effect."""
    base = pygame.Surface((width, height))
    base.fill(BLACK)
    
    # Draw the main shape
    pygame.draw.rect(base, color, (intensity, intensity, 
                                 width - 2*intensity, 
                                 height - 2*intensity))
    
    # Apply blur for glow effect
    return base

def distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    return ((point1[0] - point2[0]) ** 2 + 
            (point1[1] - point2[1]) ** 2) ** 0.5
