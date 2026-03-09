import sys
import pygame
import random
from classes.paddle import Paddle
from classes.ball import Ball
from classes.powerup_ball import PowerupBall


WIDTH, HEIGHT = 800, 600
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_RADIUS = 8


class Button:
	def __init__(self, x, y, width, height, text, color, text_color):
		self.rect = pygame.Rect(x, y, width, height)
		self.text = text
		self.color = color
		self.text_color = text_color
		self.hovered = False
	
	def draw(self, screen, font):
		# Draw button background
		pygame.draw.rect(screen, self.color, self.rect)
		# Draw button border
		pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
		# Draw text
		text_surf = font.render(self.text, True, self.text_color)
		text_rect = text_surf.get_rect(center=self.rect.center)
		screen.blit(text_surf, text_rect)
	
	def is_clicked(self, pos):
		return self.rect.collidepoint(pos)


def draw_center_line(screen):
	for y in range(0, HEIGHT, 20):
		if (y // 20) % 2 == 0:
			pygame.draw.rect(screen, (200, 200, 200), (WIDTH // 2 - 1, y, 2, 10))


def apply_powerup(paddle, powerup_type):
	"""Apply powerup effect to paddle"""
	if powerup_type == 'speed_boost':
		paddle.speed_boost_time = 10.0  # 10 seconds
		paddle.speed_boost_notification_time = 1.0  # Show message for 1 second
	elif powerup_type == 'immunity':
		paddle.immunity_count += 1
		paddle.immunity_notification_time = 1.0  # Show message for 1 second


def draw_powerup_hud(screen, paddle, font, is_left):
	"""Draw powerup HUD on left or right side of screen"""
	small_font = pygame.font.SysFont(None, 24)
	
	if is_left:
		x_pos = 50
	else:
		x_pos = WIDTH - 50
	
	# Draw speed boost notification (top of side)
	if paddle.speed_boost_notification_time > 0:
		speed_text = font.render("you got speed", True, (255, 215, 0))
		if is_left:
			screen.blit(speed_text, (x_pos, 100))
		else:
			text_rect = speed_text.get_rect()
			screen.blit(speed_text, (x_pos - text_rect.width, 100))
	
	# Draw immunity notification (top of side)
	if paddle.immunity_notification_time > 0:
		immunity_text = font.render("you got score immunity", True, (100, 255, 100))
		if is_left:
			screen.blit(immunity_text, (x_pos, 100))
		else:
			text_rect = immunity_text.get_rect()
			screen.blit(immunity_text, (x_pos - text_rect.width, 100))
	
	# Draw speed boost countdown (bottom of side)
	if paddle.speed_boost_time > 0:
		countdown = int(paddle.speed_boost_time) + 1
		countdown_text = small_font.render(str(countdown), True, (255, 215, 0))
		if is_left:
			screen.blit(countdown_text, (x_pos, HEIGHT - 50))
		else:
			text_rect = countdown_text.get_rect()
			screen.blit(countdown_text, (x_pos - text_rect.width, HEIGHT - 50))
	
	# Draw immunity count next to speed countdown (bottom of side)
	if paddle.immunity_count > 0:
		immunity_count_text = small_font.render(str(paddle.immunity_count), True, (100, 255, 100))
		if is_left:
			# Position to the right of speed countdown
			screen.blit(immunity_count_text, (x_pos + 30, HEIGHT - 50))
		else:
			# Position to the left of speed countdown
			text_rect = immunity_count_text.get_rect()
			screen.blit(immunity_count_text, (x_pos - text_rect.width - 30, HEIGHT - 50))


def init_game():
	"""Initialize game objects"""
	left = Paddle(30, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT, speed=6, color=(255, 255, 255))
	right = Paddle(WIDTH - 30 - PADDLE_WIDTH, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT, speed=6, color=(255, 255, 0))
	ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, speed=5)
	powerup_ball = None
	powerup_spawn_timer = 0
	return left, right, ball, powerup_ball, powerup_spawn_timer


def main():
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Pong - Base Version')
	clock = pygame.time.Clock()
	font = pygame.font.SysFont(None, 48)
	large_font = pygame.font.SysFont(None, 72)

	left, right, ball, powerup_ball, powerup_spawn_timer = init_game()
	
	game_over = False
	winner = None
	game_over_time = 0

	running = True
	while running:
		dt = clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					# reset scores and positions
					left, right, ball, powerup_ball, powerup_spawn_timer = init_game()
					game_over = False
					winner = None
					game_over_time = 0
			if event.type == pygame.MOUSEBUTTONDOWN:
				if game_over:
					mouse_pos = event.pos
					if play_again_button.is_clicked(mouse_pos):
						left, right, ball, powerup_ball, powerup_spawn_timer = init_game()
						game_over = False
						winner = None
						game_over_time = 0
					elif quit_button.is_clicked(mouse_pos):
						running = False

		if not game_over:
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

			# Update paddles (for speed boost timer)
			left.update(dt / 1000.0)
			right.update(dt / 1000.0)

			# Powerup ball spawn logic
			powerup_spawn_timer += dt / 1000.0
			if powerup_ball is None and powerup_spawn_timer > random.uniform(8, 15):
				powerup_ball = PowerupBall(
					WIDTH // 2,
					random.randint(50, HEIGHT - 50),
					BALL_RADIUS,
					speed=5
				)
				powerup_spawn_timer = 0

			# Update powerup ball if it exists
			if powerup_ball is not None:
				powerup_ball.update(HEIGHT, [left, right])
				# Check if paddles hit the powerup ball
				left_rect = left.get_rect()
				right_rect = right.get_rect()
				if powerup_ball.check_collision(left_rect):
					apply_powerup(left, powerup_ball.powerup_type)
					powerup_ball = None
				elif powerup_ball.check_collision(right_rect):
					apply_powerup(right, powerup_ball.powerup_type)
					powerup_ball = None
				# Remove powerup if it goes off screen
				elif powerup_ball.x < 0 or powerup_ball.x > WIDTH:
					powerup_ball = None

			# Update ball and check scoring
			scorer = ball.update(HEIGHT, [left, right])
			if scorer == 'left':
				if right.immunity_count > 0:
					right.immunity_count -= 1
				else:
					left.score += 1
				ball.reset(WIDTH // 2, HEIGHT // 2)
			elif scorer == 'right':
				if left.immunity_count > 0:
					left.immunity_count -= 1
				else:
					right.score += 1
				ball.reset(WIDTH // 2, HEIGHT // 2)
			
			# Check for win condition
			if left.score >= 10:
				game_over = True
				winner = 'white'
				game_over_time = 0
			elif right.score >= 10:
				game_over = True
				winner = 'yellow'
				game_over_time = 0

		else:
			game_over_time += dt / 1000.0

		# Draw
		screen.fill((0, 0, 0))
		
		if not game_over:
			draw_center_line(screen)
			left.draw(screen)
			right.draw(screen)
			ball.draw(screen)
			if powerup_ball is not None:
				powerup_ball.draw(screen)

			left_surf = font.render(str(left.score), True, (255, 255, 255))
			right_surf = font.render(str(right.score), True, (255, 255, 255))
			screen.blit(left_surf, (WIDTH // 2 - 100, 20))
			screen.blit(right_surf, (WIDTH // 2 + 60, 20))
			
			# Draw powerup HUDs
			draw_powerup_hud(screen, left, font, is_left=True)
			draw_powerup_hud(screen, right, font, is_left=False)
		
		else:
			# Draw win message for first 2 seconds
			if game_over_time < 2:
				if winner == 'white':
					win_text = large_font.render("white wins!", True, (255, 255, 255))
				else:
					win_text = large_font.render("yellow wins!", True, (255, 255, 0))
				
				win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
				screen.blit(win_text, win_rect)
			else:
				# Draw buttons after 2 seconds
				play_again_button = Button(WIDTH // 2 - 250, HEIGHT // 2 - 60, 200, 80, "play again?", (100, 100, 100), (255, 255, 255))
				quit_button = Button(WIDTH // 2 + 50, HEIGHT // 2 - 60, 200, 80, "quit game", (100, 100, 100), (255, 255, 255))
				
				play_again_button.draw(screen, font)
				quit_button.draw(screen, font)

		pygame.display.flip()

	pygame.quit()
	sys.exit()


if __name__ == '__main__':
	main()

