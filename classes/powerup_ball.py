import pygame
import random
from classes.ball import Ball


class PowerupBall(Ball):
    def __init__(self, x, y, radius, speed=5):
        super().__init__(x, y, radius, speed)
        self.is_powerup = True
        self.powerup_type = random.choice(['speed_boost', 'immunity'])
    
    def draw(self, screen):
        # Draw blue circle for powerup ball
        pygame.draw.circle(screen, (0, 100, 255), (int(self.x), int(self.y)), self.radius)
