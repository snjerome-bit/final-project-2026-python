import pygame
import random
import os

class Ball:
    def __init__(self, x, y, radius, speed=5):
        self.x, self.y, self.radius = x, y, radius
        self.initial_speed = speed
        self.speed = speed
        self.vx = speed * random.choice([-1, 1])
        self.vy = speed * random.choice([-1, 1]) * 0.5
        self.is_ghost = False
        self.ghost_time = 0
        self.ghost_max_time = 60  # Default 1 second (60 frames)
        self.is_supercharged = False
        
        image_path = os.path.join(os.path.dirname(__file__), '..', 'PNG', 'fire.png')
        self.fire_image = pygame.image.load(image_path).convert_alpha()
        scaled_size = int(self.radius * 2 * 10)
        self.fire_image = pygame.transform.scale(self.fire_image, (scaled_size, scaled_size))

    def update(self, screen_height, paddles):
        self.x += self.vx
        self.y += self.vy
        event_trigger = None

        if self.y - self.radius <= 0 or self.y + self.radius >= screen_height:
            self.vy = -self.vy
            if self.is_supercharged:
                event_trigger = "wall_charged"

        if self.is_ghost:
            self.ghost_time += 1
            if self.ghost_time > self.ghost_max_time:
                self.is_ghost = False
                self.ghost_time = 0

        for paddle in paddles:
            paddle_rect = paddle.get_rect()
            if self.check_collision(paddle_rect):
                if not self.is_ghost:
                    if paddle.charged_double_hit:
                        self.is_supercharged = True
                        paddle.charged_double_hit = False
                        self.speed *= 2.0
                        # Re-calculate velocity based on new speed
                        dir_x = -1 if self.vx > 0 else 1
                        self.vx = dir_x * self.speed
                        event_trigger = "hit_charged"
                    else:
                        self.speed *= 1.05
                        self.vx = -self.vx
                    
                    hit_pos = (self.y - paddle.y) / paddle.height
                    self.vy = (hit_pos - 0.5) * self.speed * 2
                    
                    if self.vx > 0: self.x = paddle_rect.right + self.radius
                    else: self.x = paddle_rect.left - self.radius
                
                paddle.meter_fill = min(2.0, paddle.meter_fill + 0.25)
                
        if self.x - self.radius <= 0: return 'right'
        elif self.x + self.radius >= 800: return 'left'
        return event_trigger

    def check_collision(self, rect):
        closest_x = max(rect.left, min(self.x, rect.right))
        closest_y = max(rect.top, min(self.y, rect.bottom))
        return ((self.x - closest_x)**2 + (self.y - closest_y)**2)**0.5 < self.radius

    def draw(self, screen):
        img = pygame.transform.flip(self.fire_image, self.vx > 0, False)
        img.set_alpha(100 if self.is_ghost else 255)
        screen.blit(img, img.get_rect(center=(int(self.x), int(self.y))))

    def reset(self, x, y):
        self.x, self.y = x, y
        self.speed = self.initial_speed
        self.vx = self.speed * random.choice([-1, 1])
        self.vy = self.speed * random.choice([-1, 1]) * 0.5
        self.is_ghost = False
        self.ghost_time = 0
        self.ghost_max_time = 60  # Reset to default 1 second
        self.is_supercharged = False
        self.ghost_time = 0