"""
Player class handling Pac-Man movement, animation, and game mechanics.
"""
import pygame
from utils import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.speed = PLAYER_SPEED
        self.radius = TILE_SIZE // 2 - 2
        self.lives = 3
        self.score = 0
        self.powered_up = False
        self.power_time = 0
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.is_dead = False
        self.is_moving = False  # Track if player is currently moving
        
        # Animation angles for mouth
        self.mouth_angle = 0
        self.mouth_speed = 5
        self.mouth_direction = 1  # 1 for opening, -1 for closing
        
    def update(self, maze):
        """Update player position and animation."""
        if self.is_dead:
            self._update_death_animation()
            return
            
        # Update mouth animation only when moving
        if self.is_moving:
            self.mouth_angle += self.mouth_speed * self.mouth_direction
            if self.mouth_angle >= 45:
                self.mouth_direction = -1
            elif self.mouth_angle <= 0:
                self.mouth_direction = 1
        else:
            # Keep mouth slightly open when not moving
            self.mouth_angle = 20
            
        # Try to change direction if requested
        if self.next_direction != self.direction:
            next_x = self.x + self.next_direction[0] * self.speed
            next_y = self.y + self.next_direction[1] * self.speed
            if maze.is_valid_position(next_x, next_y):
                self.direction = self.next_direction
        
        # Only move if player is supposed to be moving
        if self.is_moving:
            # Move in current direction
            next_x = self.x + self.direction[0] * self.speed
            next_y = self.y + self.direction[1] * self.speed
            
            # Check if the next position is valid
            if maze.is_valid_position(next_x, next_y):
                self.x = next_x
                self.y = next_y
            else:
                # Stop moving if we hit a wall
                self.is_moving = False
            
        # Check for pellet collection
        center_x = self.x + TILE_SIZE // 2
        center_y = self.y + TILE_SIZE // 2
        points = maze.eat_pellet((center_x, center_y))
        if points == POWER_PELLET_POINTS:
            self.powered_up = True
            self.power_time = pygame.time.get_ticks()
        self.score += points
        
        # Update power pellet status
        if self.powered_up:
            if pygame.time.get_ticks() - self.power_time > 6000:  # 6 seconds
                self.powered_up = False
                
    def draw(self, screen):
        """Draw Pac-Man with mouth animation."""
        if self.is_dead:
            self._draw_death_animation(screen)
            return
            
        # Calculate the angles for the Pac-Man arc
        start_angle = 0
        if self.direction == RIGHT:
            start_angle = -self.mouth_angle
        elif self.direction == LEFT:
            start_angle = 180 - self.mouth_angle
        elif self.direction == UP:
            start_angle = 90 - self.mouth_angle
        elif self.direction == DOWN:
            start_angle = 270 - self.mouth_angle
            
        # Draw Pac-Man body - use Amazon orange color
        amazon_yellow = (255, 153, 0)  # Amazon orange/yellow
        center = (int(self.x + TILE_SIZE//2), int(self.y + TILE_SIZE//2))
        pygame.draw.circle(screen, amazon_yellow, center, self.radius)
        
        # Draw mouth using a simple polygon
        if not self.mouth_angle == 0:
            # Calculate mouth points manually using math module
            import math
            angle1_rad = math.radians(start_angle - self.mouth_angle)
            angle2_rad = math.radians(start_angle + self.mouth_angle)
            
            # Calculate end points of mouth lines
            x1 = center[0] + self.radius * math.cos(angle1_rad)
            y1 = center[1] - self.radius * math.sin(angle1_rad)
            x2 = center[0] + self.radius * math.cos(angle2_rad)
            y2 = center[1] - self.radius * math.sin(angle2_rad)
            
            # Draw mouth as triangle
            pygame.draw.polygon(screen, BLACK, [center, (int(x1), int(y1)), (int(x2), int(y2))])
    
    def _update_death_animation(self):
        """Update the death animation sequence."""
        self.animation_frame += self.animation_speed
        if self.animation_frame >= 8:  # Animation complete
            self.is_dead = False
            self.animation_frame = 0
            
    def _draw_death_animation(self, screen):
        """Draw the death animation sequence."""
        import math
        center = (int(self.x + TILE_SIZE//2), int(self.y + TILE_SIZE//2))
        
        # Draw a simple circle that gets smaller as animation progresses
        radius = int(self.radius * (1 - self.animation_frame/8))
        if radius > 0:
            pygame.draw.circle(screen, (255, 153, 0), center, radius)
        
    def handle_input(self, event):
        """Handle keyboard input for movement."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.next_direction = UP
                self.is_moving = True
            elif event.key == pygame.K_DOWN:
                self.next_direction = DOWN
                self.is_moving = True
            elif event.key == pygame.K_LEFT:
                self.next_direction = LEFT
                self.is_moving = True
            elif event.key == pygame.K_RIGHT:
                self.next_direction = RIGHT
                self.is_moving = True
        elif event.type == pygame.KEYUP:
            # Stop moving when key is released
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                self.is_moving = False
                
    def die(self):
        """Start death animation and reduce lives."""
        if not self.is_dead:
            self.is_dead = True
            self.lives -= 1
            self.animation_frame = 0
            self.powered_up = False
            self.is_moving = False
            
    def reset_position(self, x, y):
        """Reset player to starting position."""
        self.x = x
        self.y = y
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.is_dead = False
        self.powered_up = False
        self.is_moving = False
