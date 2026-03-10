import pygame
import random
from classes.ball import Ball


class SuperHitBall(Ball):
    def __init__(self, x, y, radius, speed=5):
        super().__init__(x, y, radius, speed)
        self.is_powerup = True
        self.powerup_type = 'super_hit'
    
    def update(self, screen_height, paddles):
        """Update super hit ball - similar to Ball but without repositioning"""
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
        # Draw red circle for super hit powerup ball
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), self.radius)
