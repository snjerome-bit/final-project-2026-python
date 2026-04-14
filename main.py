import sys, pygame, random, os
from classes.paddle import Paddle
from classes.ball import Ball
from classes.powerup_ball import PowerupBall
from classes.particles import ParticleManager

# --- CONFIGURATION ---
WIDTH, HEIGHT = 800, 600
FPS = 60
TITLE_SCREEN, COUNTDOWN, PLAYING, GAME_OVER = 0, 1, 2, 3

class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text, self.color, self.text_color = text, color, text_color
    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=10)
        txt = font.render(self.text, True, self.text_color)
        screen.blit(txt, txt.get_rect(center=self.rect.center))
    def is_clicked(self, pos): return self.rect.collidepoint(pos)

def draw_center_line(screen):
    """Draws a classic dashed Pong line down the middle"""
    for y in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, (100, 100, 100), (WIDTH // 2 - 2, y + 10, 4, 20))

def draw_hud(screen, left, right, font):
    """Draws Score and the Blue/Red Energy Meters"""
    small_f = pygame.font.SysFont("Arial", 20)
    screen.blit(font.render(str(left.score), True, (255, 255, 255)), (WIDTH // 2 - 80, 20))
    screen.blit(font.render(str(right.score), True, (255, 255, 255)), (WIDTH // 2 + 40, 20))
    
    for p, is_l in [(left, True), (right, False)]:
        m_x = 20 if is_l else WIDTH - 120
        # Level 1 Meter (Blue)
        pygame.draw.rect(screen, (30, 30, 30), (m_x, HEIGHT-30, 100, 10))
        pygame.draw.rect(screen, (0, 200, 255), (m_x, HEIGHT-30, int(100 * min(1.0, p.meter_fill)), 10))
        # Level 2 Meter (Red)
        pygame.draw.rect(screen, (30, 30, 30), (m_x, HEIGHT-45, 100, 10))
        if p.meter_fill > 1.0:
            pygame.draw.rect(screen, (255, 50, 50), (m_x, HEIGHT-45, int(100 * (p.meter_fill - 1.0)), 10))
        if p.immunity_count > 0 or p.shield_spin_time > 0:
            # Draw shield sign with spin and bulge animation
            shield_text = small_f.render(f"SHIELDS: {p.immunity_count}", True, (100, 255, 100))
            shield_pos = (m_x, 70)
            center_x = shield_pos[0] + shield_text.get_width() // 2
            center_y = shield_pos[1] + shield_text.get_height() // 2
            
            # If shield is spinning, rotate and scale the text (bulge effect)
            if p.shield_spin_time > 0:
                # Calculate rotation angle (360 degrees in 0.5 seconds)
                rotation_angle = (1 - p.shield_spin_time / 0.5) * 360
                # Calculate bulge scale (grows then shrinks, max 1.3x at middle)
                progress = (1 - p.shield_spin_time / 0.5)  # 0 to 1
                bulge_scale = 1.0 + 0.3 * abs(0.5 - progress) * 2  # 1.0 to 1.3 and back to 1.0
                
                # Scale and rotate
                scaled_shield = pygame.transform.scale(shield_text, 
                                                      (int(shield_text.get_width() * bulge_scale), 
                                                       int(shield_text.get_height() * bulge_scale)))
                rotated_shield = pygame.transform.rotate(scaled_shield, rotation_angle)
                rotated_rect = rotated_shield.get_rect(center=(center_x, center_y))
                
                # Draw Doctor Strange portal effect - particles in ring closing inward
                import math
                import random
                num_particles = 30
                max_radius = 60
                
                
                for i in range(num_particles):
                    # Base angle for the particle to form a ring
                    base_angle = (i / num_particles) * 360
                    # Rotate with the portal for spinning effect
                    angle = base_angle + rotation_angle
                    rad = math.radians(angle)
                    
                    # Particles spiral inward - ring closes from large to small
                    current_radius = max_radius * (1 - progress)
                    
                    particle_x = center_x + math.cos(rad) * current_radius
                    particle_y = center_y + math.sin(rad) * current_radius
                    
                    # Some particles scatter and fall as portal closes
                    if progress > 0.3 and random.random() < progress * 0.5:  # More scatter as it closes
                        # Add random horizontal scatter
                        particle_x += random.uniform(-15, 15) * progress
                        # Particles fall downward
                        particle_y += (progress - 0.3) * 40
                    
                    # Fade out as animation progresses
                    particle_alpha = int(255 * (1 - progress))
                    
                    # Golden-orange color
                    particle_color = (255, 165, 0, particle_alpha)
                    
                    particle_size = 4
                    particle_surf = pygame.Surface((particle_size * 2, particle_size * 2), pygame.SRCALPHA)
                    pygame.draw.circle(particle_surf, particle_color, (particle_size, particle_size), particle_size)
                    screen.blit(particle_surf, (int(particle_x) - particle_size, int(particle_y) - particle_size))
                
                screen.blit(rotated_shield, rotated_rect)
            else:
                screen.blit(shield_text, shield_pos)
        
        # Draw speed boost timer if active
        if p.speed_boost_time > 0:
            speed_text = small_f.render(f"SPEED: {max(0, int(p.speed_boost_time))}s", True, (255, 200, 0))
            screen.blit(speed_text, (m_x, 100))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SUPER PONG")
    clock = pygame.time.Clock()
    font, big_font = pygame.font.SysFont("Arial", 24), pygame.font.SysFont("Arial", 100)
    
    # Initialize Game Objects
    left = Paddle(30, 250, 10, 100, 6, (255,255,255))
    right = Paddle(760, 250, 10, 100, 6, (255,255,0))
    ball = Ball(400, 300, 8)
    particles = ParticleManager()
    
    current_state = TITLE_SCREEN
    p_ball, p_timer = None, 0
    shield_timer = 0  # Separate timer for shield spawning
    shake_t, shake_i, countdown_timer = 0, 0, 3.0
    winner = None

    btn_start = Button(WIDTH//2-110, 350, 220, 60, "START GAME", (50, 150, 50), (255, 255, 255))
    btn_restart = Button(WIDTH//2-110, 300, 220, 60, "RESTART", (50, 150, 50), (255, 255, 255))
    btn_quit = Button(WIDTH//2-110, 380, 220, 60, "QUIT", (150, 50, 50), (255, 255, 255))

    while True:
        dt = clock.tick(FPS) / 1000.0
        canvas = pygame.Surface((WIDTH, HEIGHT))
        canvas.fill((0, 0, 0))
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            
            if current_state == TITLE_SCREEN and e.type == pygame.MOUSEBUTTONDOWN:
                if btn_start.is_clicked(e.pos):
                    # Clean Reset
                    left = Paddle(30, 250, 10, 100, 6, (255,255,255))
                    right = Paddle(760, 250, 10, 100, 6, (255,255,0))
                    ball = Ball(400, 300, 8)
                    current_state, countdown_timer = COUNTDOWN, 3.0
            
            if current_state in [PLAYING, COUNTDOWN]:
                if e.type == pygame.KEYDOWN:
                    # White Controls
                    if e.key == pygame.K_CAPSLOCK and left.meter_fill >= 1.0:
                        ball.is_ghost = True; left.meter_fill -= 1.0
                    if e.key == pygame.K_LSHIFT and left.meter_fill >= 2.0:
                        left.charged_double_hit = True; left.meter_fill = 0.0
                    # Yellow Controls
                    if e.key == pygame.K_RETURN and right.meter_fill >= 1.0:
                        ball.is_ghost = True; right.meter_fill -= 1.0
                    if e.key == pygame.K_RSHIFT and right.meter_fill >= 2.0:
                        right.charged_double_hit = True; right.meter_fill = 0.0
                    # Parry (Press Q for left, / for right to make Ghost Ball solid)
                    if e.key in [pygame.K_q, pygame.K_SLASH]:
                        if ball.is_ghost and (abs(ball.x - right.x) < 80 or abs(ball.x - left.x) < 80):
                            ball.is_ghost = False 

        # Movement
        keys = pygame.key.get_pressed()
        if current_state in [PLAYING, COUNTDOWN]:
            if keys[pygame.K_w]: left.move(-1, HEIGHT)
            if keys[pygame.K_s]: left.move(1, HEIGHT)
            if keys[pygame.K_UP]: right.move(-1, HEIGHT)
            if keys[pygame.K_DOWN]: right.move(1, HEIGHT)
            left.update(dt); right.update(dt)

        if current_state == TITLE_SCREEN:
            t_surf = big_font.render("SUPER PONG", True, (255, 255, 255))
            canvas.blit(t_surf, t_surf.get_rect(center=(WIDTH//2, 200)))
            btn_start.draw(canvas, font)

        elif current_state == COUNTDOWN:
            countdown_timer -= dt
            if countdown_timer <= 0: current_state = PLAYING
            draw_center_line(canvas)
            left.draw(canvas); right.draw(canvas); ball.draw(canvas); draw_hud(canvas, left, right, font)
            c_txt = big_font.render(str(int(countdown_timer)+1), True, (255, 50, 50))
            canvas.blit(c_txt, c_txt.get_rect(center=(WIDTH//2, HEIGHT//2)))

        elif current_state == PLAYING:
            draw_center_line(canvas)
            particles.update(dt)
            res = ball.update(HEIGHT, [left, right])
            
            if res == "hit_charged": 
                particles.emit(ball.x, ball.y); shake_t, shake_i = 0.15, 8
            elif res == "wall_charged": 
                shake_t, shake_i = 0.3, 15
            elif res in ['left', 'right']:
                # If ball is in ghost mode, it passes through without scoring or shield interaction
                if ball.is_ghost:
                    ball.reset(WIDTH//2, HEIGHT//2)
                    current_state, countdown_timer = COUNTDOWN, 3.0
                else:
                    shield_blocked = False
                    if res == 'right': # White Scored (ball went left, so left is the defender)
                        if left.immunity_count > 0: 
                            left.immunity_count -= 1
                            left.shield_spin_time = 0.5  # Spin for 0.5 seconds
                            particles.emit(ball.x, ball.y, count=50, color='green_yellow')
                            shake_t, shake_i = 0.2, 10
                            ball.vx = -ball.vx  # Bounce ball back
                            ball.is_ghost = True
                            ball.ghost_time = 0
                            ball.ghost_max_time = 60  # 1 second (60 frames at 60 FPS)
                            shield_blocked = True
                        else: 
                            right.score += 1
                            left.meter_fill = 0.0  # White's meter resets only when they actually score
                    else: # Yellow Scored (ball went right, so right is the defender)
                        if right.immunity_count > 0: 
                            right.immunity_count -= 1
                            right.shield_spin_time = 0.5  # Spin for 0.5 seconds
                            particles.emit(ball.x, ball.y, count=50, color='green_yellow')
                            shake_t, shake_i = 0.2, 10
                            ball.vx = -ball.vx  # Bounce ball back
                            ball.is_ghost = True
                            ball.ghost_time = 0
                            ball.ghost_max_time = 60  # 1 second (60 frames at 60 FPS)
                            shield_blocked = True
                        else: 
                            left.score += 1
                            right.meter_fill = 0.0  # Yellow's meter resets only when they actually score
                    
                    if not shield_blocked:
                        if left.score >= 10 or right.score >= 10:
                            winner = "White" if left.score >= 10 else "Yellow"
                            current_state = GAME_OVER
                        else:
                            ball.reset(WIDTH//2, HEIGHT//2)
                            current_state, countdown_timer = COUNTDOWN, 3.0

            # Powerups
            p_timer += dt
            shield_timer += dt
            
            # Spawn speed boosts every 30 seconds
            if not p_ball and p_timer > 30:
                p_ball = PowerupBall(WIDTH//2, random.randint(50, HEIGHT-50), 8, powerup_type='speed_boost')
                p_timer = 0
            
            # Spawn shields every 60 seconds (1 minute)
            if not p_ball and shield_timer > 60:
                p_ball = PowerupBall(WIDTH//2, random.randint(50, HEIGHT-50), 8, powerup_type='immunity')
                shield_timer = 0
            
            if p_ball:
                p_res = p_ball.update(HEIGHT, [left, right])
                p_ball.draw(canvas)
                if p_ball.check_collision(left.get_rect()): 
                    if p_ball.powerup_type == 'immunity':
                        left.immunity_count += 1
                    else:  # speed_boost
                        left.speed_boost_time = 10.0  # 10 second speed boost
                    p_ball = None
                elif p_ball and p_ball.check_collision(right.get_rect()): 
                    if p_ball.powerup_type == 'immunity':
                        right.immunity_count += 1
                    else:  # speed_boost
                        right.speed_boost_time = 10.0  # 10 second speed boost
                    p_ball = None
                elif p_res in ['left', 'right']: p_ball = None  # Ball went off screen

            left.draw(canvas); right.draw(canvas); ball.draw(canvas); particles.draw(canvas); draw_hud(canvas, left, right, font)

        elif current_state == GAME_OVER:
            g_msg = font.render(f"{winner} Wins!", True, (255,255,255))
            canvas.blit(g_msg, g_msg.get_rect(center=(WIDTH//2, 150)))
            btn_restart.draw(canvas, font)
            btn_quit.draw(canvas, font)
            
            if e.type == pygame.MOUSEBUTTONDOWN:
                if btn_restart.is_clicked(e.pos): current_state = TITLE_SCREEN
                elif btn_quit.is_clicked(e.pos): pygame.quit(); sys.exit()

        # Shake and Draw
        ox, oy = 0, 0
        if shake_t > 0:
            shake_t -= dt
            ox, oy = random.randint(-shake_i, shake_i), random.randint(-shake_i, shake_i)
        
        screen.blit(canvas, (ox, oy))
        pygame.display.flip()

if __name__ == '__main__':
    main()