import pygame
import random


class Ball:
    def __init__(self, x, y, radius, speed=5):
        self.x = x
        self.y = y
        self.radius = radius
        self.initial_speed = speed
        self.speed = speed
        self.vx = speed * random.choice([-1, 1])
        self.vy = speed * random.choice([-1, 1]) * 0.5

    def update(self, screen_height, paddles):
        self.x += self.vx
        self.y += self.vy

        if self.y - self.radius <= 0 or self.y + self.radius >= screen_height:
            self.vy = -self.vy

        for paddle in paddles:
            paddle_rect = paddle.get_rect()
            if self.check_collision(paddle_rect):
                self.vx = -self.vx
                hit_pos = (self.y - paddle.y) / paddle.height
                self.vy = (hit_pos - 0.5) * self.speed * 2
                # Increase ball speed slightly on paddle collision
                self.speed *= 1.05

        if self.x - self.radius <= 0:
            return 'right'
        elif self.x + self.radius >= 800:
            return 'left'
        return None

    def check_collision(self, rect):
        closest_x = max(rect.left, min(self.x, rect.right))
        closest_y = max(rect.top, min(self.y, rect.bottom))
        distance = ((self.x - closest_x) ** 2 + (self.y - closest_y) ** 2) ** 0.5
        return distance < self.radius

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.speed = self.initial_speed
        self.vx = self.speed * random.choice([-1, 1])
        self.vy = self.speed * random.choice([-1, 1]) * 0.5
