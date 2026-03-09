import pygame


class Paddle:
    def __init__(self, x, y, width, height, speed=6, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.initial_speed = speed
        self.score = 0
        self.color = color
        self.speed_boost_time = 0  # Time remaining for speed boost
        self.speed_boost_notification_time = 0  # Time to show "you got speed" message
        self.immunity_count = 0  # Number of immunity shields remaining
        self.immunity_notification_time = 0  # Time to show "you got score immunity" message

    def move(self, direction, screen_height):
        """Move paddle up (-1) or down (1)"""
        self.y += direction * self.speed
        self.y = max(0, min(self.y, screen_height - self.height))

    def update(self, dt):
        """Update paddle state (speed boost timer)"""
        if self.speed_boost_time > 0:
            self.speed = self.initial_speed * 2
            self.speed_boost_time -= dt
        else:
            self.speed = self.initial_speed
        
        # Update notification timers
        if self.speed_boost_notification_time > 0:
            self.speed_boost_notification_time -= dt
        if self.immunity_notification_time > 0:
            self.immunity_notification_time -= dt

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def reset(self, y):
        self.y = y

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
