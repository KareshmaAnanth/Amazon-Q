"""
Maze layout and rendering logic for the Amazon Pac-Man game.
Maze pattern with letters A, M, A, Z, O, N at top and Q, C, L, I at bottom.
"""
import pygame
import random
from utils import *

class Maze:
    def __init__(self):
        # Define the maze layout where:
        # 0 = empty path
        # 1 = wall
        # 2 = pellet
        # 3 = power pellet
        
        # Create a maze with AMAZON letters at top and Q CLI at bottom
        self.layout = self._generate_amazon_maze(45, 30)  # Extended width to 45 to fit all letters
        
        # Initialize collections for game elements
        self.walls = []
        self.pellets = []
        self.power_pellets = []
        self._initialize_elements()
        
        # Create blue pixel style wall effect
        self.wall_surface = self._create_wall_surface()
    
    def _generate_amazon_maze(self, width, height):
        """Generate a maze with AMAZON letters at top and Q CLI at bottom."""
        # Start with all paths
        maze = [[0 for x in range(width)] for y in range(height)]
        
        # Create border
        for y in range(height):
            for x in range(width):
                # Border walls
                if x == 0 or y == 0 or x == width-1 or y == height-1:
                    maze[y][x] = 1
        
        # Add letter patterns with proper spacing
        # Top row: A, M, A, Z, O, N
        # Bottom row: Q, C, L, I
        letters_top = ['A', 'M', 'A', 'Z', 'O', 'N']
        letters_bottom = ['Q', 'C', 'L', 'I']
        letter_width = 3  # Original letter width
        letter_height = 5  # Original letter height
        spacing = 4  # Spacing between letters
        
        # Calculate starting positions to center the letters
        start_x_top = 3  # Start after some space from left wall
        start_x_bottom = 8  # Start after some space from left wall for bottom row
        
        # Position for top row - moved down from the top border
        y_pos_top = 5  # Fixed position for top row
        
        # Position for bottom row - moved up from the bottom border
        y_pos_bottom = height - 10  # Fixed position for bottom row
        
        # Add top row letters (AMAZON) with spacing
        for i, letter in enumerate(letters_top):
            x_pos = start_x_top + i * (letter_width + spacing)
            self._add_letter(maze, letter, x_pos, y_pos_top)
        
        # Add bottom row letters (Q CLI) with spacing
        for i, letter in enumerate(letters_bottom):
            x_pos = start_x_bottom + i * (letter_width + spacing)
            self._add_letter(maze, letter, x_pos, y_pos_bottom)
        
        # Fill with pellets
        for y in range(height):
            for x in range(width):
                if maze[y][x] == 0:
                    maze[y][x] = 2
        
        # Add power pellets in corners and center
        power_pellet_positions = [
            (2, 2), (width-3, 2), (2, height-3), (width-3, height-3),
            (width//2, height//2)
        ]
        
        for x, y in power_pellet_positions:
            if 0 <= y < height and 0 <= x < width and maze[y][x] != 1:
                maze[y][x] = 3
                
        # Ensure starting position is clear
        maze[1][1] = 2
        maze[2][1] = 0
        maze[1][2] = 0
        
        return maze
    
    def _add_letter(self, maze, letter, x, y):
        """Add a letter pattern to the maze."""
        if letter == 'A':
            # Letter A pattern
            pattern = [
                [0,1,0],
                [1,0,1],
                [1,1,1],
                [1,0,1],
                [1,0,1]
            ]
        elif letter == 'M':
            # Letter M pattern
            pattern = [
                [1,0,1],
                [1,0,1],
                [1,1,1],
                [1,0,1],
                [1,0,1]
            ]
        elif letter == 'Z':
            # Letter Z pattern
            pattern = [
                [1,1,1],
                [0,0,1],
                [0,1,0],
                [1,0,0],
                [1,1,1]
            ]
        elif letter == 'O':
            # Letter O pattern
            pattern = [
                [1,1,1],
                [1,0,1],
                [1,0,1],
                [1,0,1],
                [1,1,1]
            ]
        elif letter == 'N':
            # Letter N pattern - made very distinct
            pattern = [
                [1,0,1],
                [1,1,1],
                [1,0,1],
                [1,0,1],
                [1,0,1]
            ]
        elif letter == 'Q':
            # Letter Q pattern - made more distinct from O with a tail
            pattern = [
                [1,1,1],
                [1,0,1],
                [1,0,1],
                [1,0,1],
                [1,1,1],
                [0,0,1]  # Added tail to make Q distinct
            ]
        elif letter == 'C':
            # Letter C pattern
            pattern = [
                [1,1,1],
                [1,0,0],
                [1,0,0],
                [1,0,0],
                [1,1,1]
            ]
        elif letter == 'L':
            # Letter L pattern
            pattern = [
                [1,0,0],
                [1,0,0],
                [1,0,0],
                [1,0,0],
                [1,1,1]
            ]
        elif letter == 'I':
            # Letter I pattern
            pattern = [
                [1,1,1],
                [0,1,0],
                [0,1,0],
                [0,1,0],
                [1,1,1]
            ]
        else:
            # Default empty pattern
            pattern = [
                [0,0,0],
                [0,0,0],
                [0,0,0],
                [0,0,0],
                [0,0,0]
            ]
        
        # Add the pattern to the maze
        for py, row in enumerate(pattern):
            for px, cell in enumerate(row):
                if 0 <= y+py < len(maze) and 0 <= x+px < len(maze[0]):
                    if cell == 1:
                        maze[y+py][x+px] = 1
        
    def _initialize_elements(self):
        """Set up initial positions of walls, pellets, and power pellets."""
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                pos = (x * TILE_SIZE + TILE_SIZE//2, 
                      y * TILE_SIZE + TILE_SIZE//2)
                if cell == 1:
                    self.walls.append(pygame.Rect(x * TILE_SIZE, 
                                                y * TILE_SIZE, 
                                                TILE_SIZE, TILE_SIZE))
                elif cell == 2:
                    self.pellets.append(pos)
                elif cell == 3:
                    self.power_pellets.append(pos)
    
    def _create_wall_surface(self):
        """Create a blue pixel style wall texture."""
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        surface.fill((0, 0, 0))  # Black background
        
        # Blue pixel style
        pixel_size = 3  # Size of each "pixel"
        blue_colors = [
            (0, 100, 255),   # Light blue
            (0, 50, 200),    # Medium blue
            (0, 0, 150)      # Dark blue
        ]
        
        # Create pixel pattern
        for y in range(0, TILE_SIZE, pixel_size):
            for x in range(0, TILE_SIZE, pixel_size):
                color = random.choice(blue_colors)
                pygame.draw.rect(surface, color, 
                               (x, y, pixel_size, pixel_size))
        
        return surface
    
    def draw(self, screen):
        """Render the maze and all its elements."""
        # Draw walls
        for wall in self.walls:
            screen.blit(self.wall_surface, wall)
        
        # Draw pellets (Amazon orange dots)
        for pellet in self.pellets:
            pygame.draw.circle(screen, (255, 153, 0), pellet, 2)
        
        # Draw power pellets with pulsing effect (Amazon blue)
        pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500.0
        size = 4 + pulse * 3
        for power_pellet in self.power_pellets:
            pygame.draw.circle(screen, (0, 155, 255), power_pellet, size)
    
    def check_collision(self, rect):
        """Check if the given rectangle collides with any walls."""
        return any(wall.colliderect(rect) for wall in self.walls)
    
    def eat_pellet(self, pos):
        """Try to eat a pellet or power pellet at the given position."""
        # Find the closest pellet within a certain radius
        radius = 10  # Detection radius
        
        for i, pellet in enumerate(self.pellets):
            if distance(pos, pellet) < radius:
                self.pellets.pop(i)
                return PELLET_POINTS
                
        for i, power_pellet in enumerate(self.power_pellets):
            if distance(pos, power_pellet) < radius:
                self.power_pellets.pop(i)
                return POWER_PELLET_POINTS
                
        return 0
    
    def get_tile_position(self, x, y):
        """Convert pixel coordinates to grid position."""
        return (x // TILE_SIZE, y // TILE_SIZE)
    
    def is_valid_position(self, x, y):
        """Check if the given position is a valid movement position."""
        # Create a rect for the player at the new position
        player_rect = pygame.Rect(x, y, TILE_SIZE-4, TILE_SIZE-4)
        
        # Check if this rect collides with any walls
        if any(wall.colliderect(player_rect) for wall in self.walls):
            return False
            
        # Also check grid position
        tile_x, tile_y = self.get_tile_position(x, y)
        if (0 <= tile_y < len(self.layout) and 
            0 <= tile_x < len(self.layout[0])):
            return self.layout[tile_y][tile_x] != 1
            
        return False
    
    def get_valid_moves(self, current_pos):
        """Get list of valid movement directions from current position."""
        valid_moves = []
        x, y = current_pos
        for dx, dy in [UP, DOWN, LEFT, RIGHT]:
            new_x = x + dx * TILE_SIZE
            new_y = y + dy * TILE_SIZE
            if self.is_valid_position(new_x, new_y):
                valid_moves.append((dx, dy))
        return valid_moves
    
    def remaining_pellets(self):
        """Get the total number of uneaten pellets."""
        return len(self.pellets) + len(self.power_pellets)
