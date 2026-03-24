import pygame
import random
import os


class Ball:
    def __init__(self, x, y, radius, speed=5):
        self.x = x
        self.y = y
        self.radius = radius
        self.initial_speed = speed
        self.speed = speed
        self.vx = speed * random.choice([-1, 1])
        self.vy = speed * random.choice([-1, 1]) * 0.5
        self.is_ghost = False  # Whether ball is in ghost mode (passes through paddles)
        self.ghost_time = 0  # How long ball has been ghost
        
        # Load fire image
        image_path = os.path.join(os.path.dirname(__file__), '..', 'PNG', 'fire.png')
        self.fire_image = pygame.image.load(image_path).convert_alpha()
        # Scale the image to fit the ball radius (10x bigger)
        scaled_size = int(self.radius * 2 * 10)
        self.fire_image = pygame.transform.scale(self.fire_image, (scaled_size, scaled_size))

    def update(self, screen_height, paddles):
        self.x += self.vx
        self.y += self.vy

        if self.y - self.radius <= 0 or self.y + self.radius >= screen_height:
            self.vy = -self.vy

        # Update ghost ball timer
        if self.is_ghost:
            self.ghost_time += 1
            if self.ghost_time > 60:  # Ghost ball lasts ~1 second at 60 FPS
                self.is_ghost = False
                self.ghost_time = 0

        for paddle in paddles:
            paddle_rect = paddle.get_rect()
            if self.check_collision(paddle_rect):
                # Only bounce if not ghost mode
                if not self.is_ghost:
                    self.vx = -self.vx
                    hit_pos = (self.y - paddle.y) / paddle.height
                    self.vy = (hit_pos - 0.5) * self.speed * 2
                    
                    # Apply double hit multiplier if active
                    if paddle.charged_double_hit:
                        self.speed *= 2.0
                        paddle.charged_double_hit = False
                    else:
                        # Increase ball speed slightly on paddle collision
                        self.speed *= 1.05
                    
                    # Move ball away from paddle to prevent multiple collisions
                    if self.vx > 0:
                        self.x = paddle_rect.right + self.radius
                    else:
                        self.x = paddle_rect.left - self.radius
                
                # Fill meter for hitting paddle
                paddle.meter_fill = min(1.0, paddle.meter_fill + 0.15)
                
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
        # Flip the image if moving right (vx > 0)
        if self.vx > 0:
            # Flip upside down
            flipped_image = pygame.transform.flip(self.fire_image, False, True)
        else:
            # Keep original orientation
            flipped_image = self.fire_image
        
        # If ghost mode, reduce opacity
        if self.is_ghost:
            flipped_image.set_alpha(100)  # ~40% opacity
        else:
            flipped_image.set_alpha(255)  # Full opacity
        
        # Draw the fire image at the ball's position
        image_rect = flipped_image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(flipped_image, image_rect)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.speed = self.initial_speed
        self.vx = self.speed * random.choice([-1, 1])
        self.vy = self.speed * random.choice([-1, 1]) * 0.5
        self.is_ghost = False
        self.ghost_time = 0
        # Re-scale the image to maintain proportions (10x bigger)
        image_path = os.path.join(os.path.dirname(__file__), '..', 'PNG', 'fire.png')
        self.fire_image = pygame.image.load(image_path).convert_alpha()
        scaled_size = int(self.radius * 2 * 10)
        self.fire_image = pygame.transform.scale(self.fire_image, (scaled_size, scaled_size))
