import pygame
import random

class Particle:
    def __init__(self, x, y, color_type='red_orange'):
        self.x, self.y = x, y
        self.vx, self.vy = random.uniform(-8, 8), random.uniform(-8, 8)
        self.lifetime = 2.0
        
        if color_type == 'red_orange':
            self.color = random.choice([(255, 0, 0), (255, 140, 0), (255, 69, 0)])
        elif color_type == 'green_yellow':
            self.color = random.choice([(0, 255, 0), (255, 255, 0), (144, 238, 144)])
        else:
            self.color = (255, 255, 255)
        
        self.size = random.randint(3, 7)

    def update(self, dt):
        self.lifetime -= dt
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        if self.lifetime > 0:
            alpha = max(0, min(255, int((self.lifetime / 2.0) * 255)))
            surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.rect(surf, (*self.color, alpha), (0, 0, self.size, self.size))
            screen.blit(surf, (int(self.x), int(self.y)))

class ParticleManager:
    def __init__(self):
        self.particles = []
    
    def emit(self, x, y, count=40, color='red_orange'):
        for _ in range(count): 
            self.particles.append(Particle(x, y, color_type=color))
    
    def update(self, dt):
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for p in self.particles: 
            p.update(dt)
    
    def draw(self, screen):
        for p in self.particles: 
            p.draw(screen)