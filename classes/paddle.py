import pygame


class Paddle:
    def __init__(self, x, y, width, height, speed=6):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.score = 0

    def move(self, direction, screen_height):
        """Move paddle up (-1) or down (1)"""
        self.y += direction * self.speed
        self.y = max(0, min(self.y, screen_height - self.height))

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))

    def reset(self, y):
        self.y = y

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
