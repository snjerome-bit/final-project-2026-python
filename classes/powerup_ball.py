import pygame
import random
from classes.ball import Ball


class PowerupBall(Ball):
    def __init__(self, x, y, radius, speed=5, powerup_type=None):
        super().__init__(x, y, radius, speed)
        self.is_powerup = True
        # If powerup_type is specified, use it; otherwise randomly choose
        if powerup_type:
            self.powerup_type = powerup_type
        else:
            # 80% speed boost, 20% immunity shield
            self.powerup_type = 'speed_boost' if random.random() < 0.8 else 'immunity'
    
    def update(self, screen_height, paddles):
        """Update powerup ball - similar to Ball but without repositioning"""
        self.x += self.vx
        self.y += self.vy

        if self.y - self.radius <= 0 or self.y + self.radius >= screen_height:
            self.vy = -self.vy

        # Don't check paddle collisions here - let main.py handle it
        # Just check screen boundaries
        if self.x - self.radius <= 0:
            return 'right'
        elif self.x + self.radius >= 800:
            return 'left'
        return None
    
    def draw(self, screen):
        # Draw bright blue circle for powerup ball
        pygame.draw.circle(screen, (0, 200, 255), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (50, 150, 255), (int(self.x), int(self.y)), self.radius, 2)
