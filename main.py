import sys, pygame, random, os
from classes.paddle import Paddle
from classes.ball import Ball
from classes.powerup_ball import PowerupBall
from classes.particles import ParticleManager

WIDTH, HEIGHT = 800, 600
FPS = 60
TITLE_SCREEN, COUNTDOWN, PLAYING, GAME_OVER = 0, 1, 2, 3

class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text, self.color, self.text_color = text, color, text_color
    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        txt = font.render(self.text, True, self.text_color)
        screen.blit(txt, txt.get_rect(center=self.rect.center))
    def is_clicked(self, pos): return self.rect.collidepoint(pos)

def main():
    # --- MAC AUDIO FIX ---
    pygame.mixer.pre_init(44100, -16, 2, 512) 
    pygame.init()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    music_file = os.path.join(script_dir, "background_music.mp3")
    
    music_status = "❌ NO FILE"
    if os.path.exists(music_file):
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play(-1)
            music_status = "🔊 MUSIC ACTIVE"
        except Exception as e:
            music_status = f"⚠️ ERROR: {str(e)[:15]}"
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 30)
    big_font = pygame.font.SysFont("Arial", 100)
    
    current_state, left, right, ball = TITLE_SCREEN, Paddle(30, 250, 10, 100, 6, (255,255,255)), Paddle(760, 250, 10, 100, 6, (255,255,0)), Ball(400, 300, 8)
    countdown_timer, game_over_timer = 3.0, 0

    while True:
        dt = clock.tick(FPS) / 1000.0
        screen.fill((0, 0, 0))
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if current_state == TITLE_SCREEN and e.type == pygame.MOUSEBUTTONDOWN:
                current_state, countdown_timer = COUNTDOWN, 3.0
            if current_state == GAME_OVER and e.type == pygame.MOUSEBUTTONDOWN:
                left.score, right.score = 0, 0
                current_state, countdown_timer = COUNTDOWN, 3.0

        # Movement (Always enabled)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: left.move(-1, HEIGHT)
        if keys[pygame.K_s]: left.move(1, HEIGHT)
        if keys[pygame.K_UP]: right.move(-1, HEIGHT)
        if keys[pygame.K_DOWN]: right.move(1, HEIGHT)
        left.update(dt); right.update(dt)

        if current_state == TITLE_SCREEN:
            txt = big_font.render("PONG", True, (255,255,255))
            screen.blit(txt, txt.get_rect(center=(WIDTH//2, HEIGHT//2-50)))
            sub = font.render("Click to Play", True, (200,200,200))
            screen.blit(sub, sub.get_rect(center=(WIDTH//2, HEIGHT//2+50)))

        elif current_state == COUNTDOWN:
            countdown_timer -= dt
            if countdown_timer <= 0: current_state = PLAYING
            left.draw(screen); right.draw(screen); ball.draw(screen)
            c = big_font.render(str(int(countdown_timer)+1), True, (255,0,0))
            screen.blit(c, c.get_rect(center=(WIDTH//2, HEIGHT//2)))

        elif current_state == PLAYING:
            res = ball.update(HEIGHT, [left, right])
            if res in ['left', 'right']:
                if res == 'right': right.score += 1
                else: left.score += 1
                if left.score >= 10 or right.score >= 10: current_state, winner = GAME_OVER, ("White" if left.score >= 10 else "Yellow")
                else: ball.reset(WIDTH//2, HEIGHT//2); current_state, countdown_timer = COUNTDOWN, 3.0
            left.draw(screen); right.draw(screen); ball.draw(screen)
            # Draw Scores
            screen.blit(font.render(str(left.score), True, (255,255,255)), (WIDTH//2-50, 20))
            screen.blit(font.render(str(right.score), True, (255,255,255)), (WIDTH//2+30, 20))

        elif current_state == GAME_OVER:
            msg = font.render(f"{winner} Wins! Click to Restart", True, (255,255,255))
            screen.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2)))

        # Visual Debug: Tells you exactly what the music is doing
        status_color = (0,255,0) if "ACTIVE" in music_status else (255,0,0)
        debug_txt = font.render(music_status, True, status_color)
        screen.blit(debug_txt, (10, 10))
        
        pygame.display.flip()

if __name__ == '__main__': main()