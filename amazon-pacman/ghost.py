"""
Ghost class implementing different AI behaviors for the enemy ghosts.
"""
import pygame
import random
from utils import *

class Ghost:
    def __init__(self, x, y, color, behavior):
        self.x = x
        self.y = y
        self.color = color
        self.behavior = behavior
        self.direction = RIGHT
        self.speed = GHOST_SPEED
        self.scared = False
        self.scared_timer = 0
        self.home_position = (x, y)
        self.target = None
        self.state = "scatter"  # scatter, chase, or frightened
        self.state_timer = pygame.time.get_ticks()
        self.state_duration = {
            "scatter": 7000,  # 7 seconds
            "chase": 20000,   # 20 seconds
        }
        self.stuck_counter = 0  # Counter to detect when ghost is stuck
        self.last_position = (x, y)  # Track last position to detect if stuck
        self.last_direction_change = pygame.time.get_ticks()
        self.is_moving = True  # Flag to ensure ghost is always moving
        
    def update(self, maze, player):
        """Update ghost position and state."""
        current_time = pygame.time.get_ticks()
        
        # Update ghost state
        if not self.scared:
            if current_time - self.state_timer > self.state_duration[self.state]:
                self.state = "chase" if self.state == "scatter" else "scatter"
                self.state_timer = current_time
        else:
            if current_time - self.scared_timer > 6000:  # 6 seconds
                self.scared = False
                
        # Update target based on behavior and state
        self.update_target(player)
        
        # Get valid moves
        valid_moves = maze.get_valid_moves((self.x, self.y))
        
        # Check if ghost is stuck (same position for multiple frames)
        current_position = (self.x, self.y)
        if current_position == self.last_position:
            self.stuck_counter += 1
        else:
            self.stuck_counter = 0
            self.last_position = current_position
        
        # If stuck or no valid moves, teleport to a safe location
        if self.stuck_counter > 5 or not valid_moves:
            self.teleport_to_safe_location(maze)
            return
            
        # Force direction change periodically to prevent looping patterns
        if current_time - self.last_direction_change > 3000:  # 3 seconds
            self.direction = self.get_random_direction(valid_moves)
            self.last_direction_change = current_time
        elif valid_moves:
            if self.scared:
                # Random movement when scared
                self.direction = random.choice(valid_moves)
            else:
                # Choose direction that gets closest to target
                self.direction = self.get_best_move(valid_moves)
                
        # Move ghost
        next_x = self.x + self.direction[0] * self.speed
        next_y = self.y + self.direction[1] * self.speed
        
        if maze.is_valid_position(next_x, next_y):
            self.x = next_x
            self.y = next_y
            self.is_moving = True
        else:
            # If can't move in current direction, pick a new one
            if valid_moves:
                self.direction = random.choice(valid_moves)
                self.is_moving = True
            else:
                self.is_moving = False
    
    def get_random_direction(self, valid_moves):
        """Get a random direction, avoiding the current one if possible."""
        if not valid_moves:
            return self.direction
            
        if len(valid_moves) > 1:
            # Try to avoid the current direction
            new_moves = [move for move in valid_moves if move != self.direction]
            if new_moves:
                return random.choice(new_moves)
                
        return random.choice(valid_moves)
    
    def teleport_to_safe_location(self, maze):
        """Teleport ghost to a safe location when stuck."""
        # Try to find a safe spot in the center area
        safe_spots = []
        for y in range(len(maze.layout)):
            for x in range(len(maze.layout[0])):
                if maze.layout[y][x] == 0 or maze.layout[y][x] == 2:
                    # Convert to pixel coordinates
                    px = x * TILE_SIZE
                    py = y * TILE_SIZE
                    safe_spots.append((px, py))
        
        if safe_spots:
            # Choose a random safe spot
            self.x, self.y = random.choice(safe_spots)
            self.stuck_counter = 0
            self.last_direction_change = pygame.time.get_ticks()
            
            # Pick a random direction
            self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
            
    def update_target(self, player):
        """Update target position based on behavior and state."""
        if self.scared:
            self.target = self.get_random_target()
            return
            
        if self.state == "scatter":
            self.target = self.home_position
            return
            
        # Chase behavior varies by ghost type
        if self.behavior == "chase":
            # Direct chase - target player's position
            if player and hasattr(player, 'x') and hasattr(player, 'y'):
                self.target = (player.x, player.y)
            else:
                self.target = self.get_random_target()
        elif self.behavior == "ambush":
            # Ambush - target 4 tiles ahead of player
            if player and hasattr(player, 'x') and hasattr(player, 'y') and hasattr(player, 'direction'):
                self.target = (player.x + player.direction[0] * 4 * TILE_SIZE,
                             player.y + player.direction[1] * 4 * TILE_SIZE)
            else:
                self.target = self.get_random_target()
        else:  # random behavior
            if random.random() < 0.1:  # 10% chance to change target
                self.target = self.get_random_target()
                
    def get_best_move(self, valid_moves):
        """Choose the move that gets closest to the target."""
        best_distance = float('inf')
        best_move = valid_moves[0]
        
        # Ensure target is not None
        if self.target is None:
            self.target = self.get_random_target()
        
        for move in valid_moves:
            next_x = self.x + move[0] * TILE_SIZE
            next_y = self.y + move[1] * TILE_SIZE
            
            # Avoid reversing direction unless necessary
            if (move[0] == -self.direction[0] and 
                move[1] == -self.direction[1] and 
                len(valid_moves) > 1):
                continue
                
            dist = distance((next_x, next_y), self.target)
            if dist < best_distance:
                best_distance = dist
                best_move = move
                
        return best_move
        
    def get_random_target(self):
        """Get a random position on the maze."""
        return (random.randint(1, 26) * TILE_SIZE,
                random.randint(1, 22) * TILE_SIZE)
        
    def draw(self, screen):
        """Draw the ghost."""
        ghost_rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
        
        # Draw body
        color = (0, 0, 255) if self.scared else self.color
        pygame.draw.ellipse(screen, color, ghost_rect)
        
        # Draw base
        base_rect = pygame.Rect(self.x, self.y + TILE_SIZE//2,
                              TILE_SIZE, TILE_SIZE//2)
        pygame.draw.rect(screen, color, base_rect)
        
        # Draw waves at bottom
        wave_points = []
        for i in range(3):
            x1 = self.x + (i * TILE_SIZE//3)
            x2 = self.x + ((i + 1) * TILE_SIZE//3)
            y1 = self.y + TILE_SIZE
            y2 = self.y + TILE_SIZE - 4
            wave_points.extend([(x1, y1), (x1 + TILE_SIZE//6, y2)])
        wave_points.append((self.x + TILE_SIZE, self.y + TILE_SIZE))
        pygame.draw.lines(screen, color, False, wave_points)
        
        # Draw eyes
        eye_color = WHITE if not self.scared else (255, 0, 0)
        eye_radius = TILE_SIZE // 6
        left_eye_pos = (self.x + TILE_SIZE//3, self.y + TILE_SIZE//3)
        right_eye_pos = (self.x + 2*TILE_SIZE//3, self.y + TILE_SIZE//3)
        pygame.draw.circle(screen, eye_color, left_eye_pos, eye_radius)
        pygame.draw.circle(screen, eye_color, right_eye_pos, eye_radius)
        
    def make_scared(self):
        """Make the ghost enter frightened state."""
        self.scared = True
        self.scared_timer = pygame.time.get_ticks()
        
    def reset_position(self):
        """Reset ghost to starting position."""
        self.x, self.y = self.home_position
        self.scared = False
        self.state = "scatter"
        self.state_timer = pygame.time.get_ticks()
        self.stuck_counter = 0
        self.last_direction_change = pygame.time.get_ticks()
        self.is_moving = True
