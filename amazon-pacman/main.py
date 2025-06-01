"""
Main game loop and initialization for Amazon Pac-Man.
"""
import pygame
import sys
import os
import time
import random
from utils import *
from maze import Maze
from player import Player
from ghost import Ghost

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Amazon Pac-Man")
        
        # Adjust screen size to fit the larger maze
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        # Create game objects
        self.maze = Maze()
        self.player = Player(TILE_SIZE, TILE_SIZE)
        
        # Create ghosts with different behaviors at random positions
        self.ghosts = self._create_ghosts()
        
        self.state = STATE_INTRO
        self.paused = False
        self.death_message_timer = 0
        self.show_death_message = False
        
        # Create assets directory if it doesn't exist
        if not os.path.exists(ASSET_DIR):
            os.makedirs(ASSET_DIR)
    
    def _create_ghosts(self):
        """Create ghosts at random valid positions."""
        ghosts = []
        colors = [
            (255, 0, 0),      # Red
            (255, 182, 255),  # Pink
            (0, 255, 255),    # Cyan
            (255, 184, 82)    # Orange
        ]
        behaviors = ["chase", "ambush", "random", "random"]
        
        # Find valid starting positions
        valid_positions = []
        for y in range(5, 20):
            for x in range(5, 23):
                if self.maze.layout[y][x] != 1:  # Not a wall
                    valid_positions.append((x * TILE_SIZE, y * TILE_SIZE))
        
        # Ensure we have enough positions
        if len(valid_positions) < 4:
            valid_positions = [(5*TILE_SIZE, 5*TILE_SIZE), 
                              (20*TILE_SIZE, 5*TILE_SIZE),
                              (5*TILE_SIZE, 18*TILE_SIZE),
                              (20*TILE_SIZE, 18*TILE_SIZE)]
        
        # Create ghosts
        for i in range(4):
            if valid_positions:
                pos = random.choice(valid_positions)
                valid_positions.remove(pos)
            else:
                pos = (random.randint(5, 20) * TILE_SIZE, 
                      random.randint(5, 18) * TILE_SIZE)
                
            ghosts.append(Ghost(pos[0], pos[1], colors[i], behaviors[i]))
            
        return ghosts
            
    def handle_events(self):
        """Process game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_RETURN:
                    if self.state == STATE_INTRO:
                        self.state = STATE_PLAYING
                    elif self.state == STATE_PLAYER_DEAD:
                        self.state = STATE_PLAYING
                
            # Pass all events to player for movement handling
            if self.state == STATE_PLAYING:
                self.player.handle_input(event)
                    
        return True
        
    def update(self):
        """Update game state."""
        if self.state == STATE_PLAYER_DEAD:
            # Check if it's time to continue
            if pygame.time.get_ticks() - self.death_message_timer > 2000:  # 2 seconds
                self.show_death_message = False
                self.state = STATE_PLAYING
                self.reset_positions()
            return
            
        if self.state != STATE_PLAYING or self.paused:
            return
            
        # Update player
        self.player.update(self.maze)
        
        # Update ghosts
        for ghost in self.ghosts:
            ghost.update(self.maze, self.player)
            
            # Check for collisions with player
            if self.check_collision(ghost):
                if ghost.scared:
                    ghost.reset_position()
                    self.player.score += GHOST_POINTS
                else:
                    self.player.die()
                    if self.player.lives <= 0:
                        self.state = STATE_GAME_OVER
                    else:
                        # Show death message
                        self.state = STATE_PLAYER_DEAD
                        self.show_death_message = True
                        self.death_message_timer = pygame.time.get_ticks()
                        
        # Check if all pellets are collected
        if self.maze.remaining_pellets() == 0:
            self.state = STATE_GAME_OVER
            
    def draw(self):
        """Render the game screen."""
        self.screen.fill(BLACK)
        
        if self.state == STATE_INTRO:
            self.draw_intro()
        elif self.state == STATE_GAME_OVER:
            self.draw_game_over()
        else:
            # Draw game elements
            self.maze.draw(self.screen)
            self.player.draw(self.screen)
            for ghost in self.ghosts:
                ghost.draw(self.screen)
                
            # Draw HUD
            self.draw_hud()
            
            # Draw death message if needed
            if self.state == STATE_PLAYER_DEAD and self.show_death_message:
                self.draw_death_message()
                
            if self.paused:
                self.draw_pause_screen()
                
        pygame.display.flip()
        
    def draw_intro(self):
        """Draw the intro screen."""
        title = "AMAZON ARCADE"
        subtitle = "PAC-MAN"
        start_text = "Press ENTER to Start"
        controls = [
            "Controls:",
            "Arrow Keys - Move (hold to continue moving)",
            "Release Arrow Keys to stop",
            "P - Pause",
            "R - Restart",
            "ESC - Quit"
        ]
        
        # Draw title with Amazon colors
        amazon_orange = (255, 153, 0)
        amazon_blue = (0, 155, 255)
        
        # Draw Amazon smile logo
        self._draw_amazon_logo(SCREEN_WIDTH//2 - 75, 50, 150)
        
        # Draw title
        draw_text(self.screen, title, 48, SCREEN_WIDTH//2, 150, amazon_blue)
        draw_text(self.screen, subtitle, 36, SCREEN_WIDTH//2, 200, amazon_orange)
        
        # Draw controls
        y = 280
        for line in controls:
            draw_text(self.screen, line, 24, SCREEN_WIDTH//2, y)
            y += 40
            
        # Draw start prompt
        draw_text(self.screen, start_text, 30, SCREEN_WIDTH//2, 500, amazon_blue)
        
    def _draw_amazon_logo(self, x, y, width):
        """Draw the Amazon smile logo."""
        amazon_orange = (255, 153, 0)
        
        # Draw the smile/arrow
        height = width // 3
        
        # Draw the curved arrow (smile)
        start_point = (x, y + height//2)
        mid_point = (x + width//2, y + height)
        end_point = (x + width, y)
        
        points = [start_point, mid_point, end_point]
        pygame.draw.lines(self.screen, amazon_orange, False, points, 4)
        
    def draw_game_over(self):
        """Draw the game over screen."""
        amazon_orange = (255, 153, 0)
        
        if self.maze.remaining_pellets() == 0:
            text = "YOU WIN!"
        else:
            text = "GAME OVER"
            
        draw_text(self.screen, text, 48, SCREEN_WIDTH//2, SCREEN_HEIGHT//3, amazon_orange)
        draw_text(self.screen, f"Score: {self.player.score}", 36,
                 SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        draw_text(self.screen, "Press R to Restart", 24,
                 SCREEN_WIDTH//2, SCREEN_HEIGHT*2//3)
    
    def draw_death_message(self):
        """Draw the player death message."""
        # Semi-transparent overlay
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        s.set_alpha(180)
        s.fill(BLACK)
        self.screen.blit(s, (0,0))
        
        # Draw message
        amazon_orange = (255, 153, 0)
        draw_text(self.screen, "PLAYER DEAD!", 48, SCREEN_WIDTH//2, SCREEN_HEIGHT//3, amazon_orange)
        draw_text(self.screen, f"Lives left: {self.player.lives}", 36, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        draw_text(self.screen, "Press ENTER to continue", 24, SCREEN_WIDTH//2, SCREEN_HEIGHT*2//3)
        
    def draw_hud(self):
        """Draw the heads-up display."""
        amazon_orange = (255, 153, 0)
        
        # Draw score at the bottom right (moved up by 2 steps)
        score_text = f"Score: {self.player.score}"
        draw_text(self.screen, score_text, 24, SCREEN_WIDTH-100, SCREEN_HEIGHT-70, amazon_orange)
        
        # Draw lives count text on the right top
        lives_text = f"LIFE COUNT: {self.player.lives}"
        draw_text(self.screen, lives_text, 24, SCREEN_WIDTH-100, 10, amazon_orange)
        
        # Draw visual representation of lives (orange player emojis) below the text
        # Create a background for the player emojis to ensure they're visible
        emoji_bg = pygame.Surface((self.player.lives * 30 + 10, 30))
        emoji_bg.fill(BLACK)
        emoji_bg.set_alpha(200)
        self.screen.blit(emoji_bg, (SCREEN_WIDTH-160, 30))
        
        for i in range(self.player.lives):
            # Draw small pacman icons (orange player emojis)
            center_x = SCREEN_WIDTH - 150 + (i * 30)
            center_y = 45  # Below the text
            radius = 10
            
            # Draw pacman body (orange)
            pygame.draw.circle(self.screen, amazon_orange, (center_x, center_y), radius)
            
            # Draw mouth
            pygame.draw.polygon(self.screen, BLACK, [
                (center_x, center_y),
                (center_x + radius, center_y - radius//2),
                (center_x + radius, center_y + radius//2)
            ])
        
    def draw_pause_screen(self):
        """Draw the pause screen overlay."""
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        s.set_alpha(128)
        s.fill(BLACK)
        self.screen.blit(s, (0,0))
        draw_text(self.screen, "PAUSED", 48, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        
    def check_collision(self, ghost):
        """Check for collision between player and ghost."""
        ghost_rect = pygame.Rect(ghost.x, ghost.y, TILE_SIZE, TILE_SIZE)
        player_rect = pygame.Rect(self.player.x, self.player.y,
                                TILE_SIZE, TILE_SIZE)
        return ghost_rect.colliderect(player_rect)
        
    def reset_positions(self):
        """Reset player and ghost positions."""
        self.player.reset_position(TILE_SIZE, TILE_SIZE)
        for ghost in self.ghosts:
            ghost.reset_position()
            
    def reset_game(self):
        """Reset the entire game state."""
        self.maze = Maze()
        self.player = Player(TILE_SIZE, TILE_SIZE)
        self.ghosts = self._create_ghosts()
        self.state = STATE_PLAYING
        self.paused = False
        self.show_death_message = False
        
    def run(self):
        """Main game loop."""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
