import sys
import pygame
from classes.paddle import Paddle
from classes.ball import Ball


WIDTH, HEIGHT = 800, 600
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_RADIUS = 8


def draw_center_line(screen):
	for y in range(0, HEIGHT, 20):
		if (y // 20) % 2 == 0:
			pygame.draw.rect(screen, (200, 200, 200), (WIDTH // 2 - 1, y, 2, 10))


def main():
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Pong - Base Version')
	clock = pygame.time.Clock()
	font = pygame.font.SysFont(None, 48)

	left = Paddle(30, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT, speed=6)
	right = Paddle(WIDTH - 30 - PADDLE_WIDTH, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT, speed=6)
	ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, speed=5)

	running = True
	while running:
		dt = clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					# reset scores and positions
					left.score = 0
					right.score = 0
					left.reset((HEIGHT - PADDLE_HEIGHT) // 2)
					right.reset((HEIGHT - PADDLE_HEIGHT) // 2)
					ball.reset(WIDTH // 2, HEIGHT // 2)

		keys = pygame.key.get_pressed()
		# Left paddle: W/S
		if keys[pygame.K_w]:
			left.move(-1, HEIGHT)
		if keys[pygame.K_s]:
			left.move(1, HEIGHT)
		# Right paddle: Up/Down
		if keys[pygame.K_UP]:
			right.move(-1, HEIGHT)
		if keys[pygame.K_DOWN]:
			right.move(1, HEIGHT)

		# Update ball and check scoring
		scorer = ball.update(HEIGHT, [left, right])
		if scorer == 'left':
			left.score += 1
			ball.reset(WIDTH // 2, HEIGHT // 2)
		elif scorer == 'right':
			right.score += 1
			ball.reset(WIDTH // 2, HEIGHT // 2)

		# Draw
		screen.fill((0, 0, 0))
		draw_center_line(screen)
		left.draw(screen)
		right.draw(screen)
		ball.draw(screen)

		left_surf = font.render(str(left.score), True, (255, 255, 255))
		right_surf = font.render(str(right.score), True, (255, 255, 255))
		screen.blit(left_surf, (WIDTH // 2 - 100, 20))
		screen.blit(right_surf, (WIDTH // 2 + 60, 20))

		pygame.display.flip()

	pygame.quit()
	sys.exit()


if __name__ == '__main__':
	main()

