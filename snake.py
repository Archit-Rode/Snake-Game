import pygame
import random
pygame.init()
# Set up display
WIDTH, HEIGHT = 800, 400
BLOCK_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRID_COLOR = (0, 40, 40)
BLACK = (0, 0, 0)
BODY_COLOR = (0, 180, 0)  # Medium green body
# Load snake head image
snake_head_img = pygame.image.load("snake3.png").convert_alpha()
snake_head_img = pygame.transform.scale(snake_head_img, (BLOCK_SIZE, BLOCK_SIZE))  # Resize image
# Snake properties
snake_body = [(WIDTH // 2, HEIGHT // 2)]  # Start with head only
snake_direction = "RIGHT"
snake_speed = 5
speed_increment = 0.25
# Food
food = (random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE))
# Score and High Score (only for current session)
score = 0
high_score = 0  # This will persist until the game is closed
font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()
def draw_grid():
    """Draws a grid on the screen."""
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))
def draw_snake():
    """Draw a continuous snake body with a smooth effect."""
    if len(snake_body) > 1:
        pygame.draw.lines(screen, BODY_COLOR, False, [(x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2) for x, y in snake_body], BLOCK_SIZE - 4)
    # Draw the snake head image
    head_x, head_y = snake_body[0]
    screen.blit(snake_head_img, (head_x, head_y))
def show_game_over():
    """Display 'Game Over' message and restart button."""
    global high_score, score
    # Update high score if the current score is greater
    if score > high_score:
        high_score = score
    font_large = pygame.font.Font(None, 50)
    font_small = pygame.font.Font(None, 30)
    button_font = pygame.font.Font(None, 35)
    text_game_over = font_large.render("Game Over", True, RED)
    text_game_over_rect = text_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    text_score = font_small.render(f"Score: {score}", True, WHITE)
    text_score_rect = text_score.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    text_high_score = font_small.render(f"High Score: {high_score}", True, WHITE)
    text_high_score_rect = text_high_score.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    button_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 80, 120, 40)
    while True:
        screen.fill(BLACK)
        screen.blit(text_game_over, text_game_over_rect)
        screen.blit(text_score, text_score_rect)
        screen.blit(text_high_score, text_high_score_rect)
        # Draw Restart button
        pygame.draw.rect(screen, WHITE, button_rect)
        button_text = button_font.render("Restart", True, BLACK)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)
        pygame.display.flip()
        # Event loop to wait for user action
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return True  # Signal to restart the game
def restart_game():
    """Reset game variables and restart but keep high score."""
    global snake_body, snake_direction, snake_speed, food, score
    # Reset snake
    snake_body = [(WIDTH // 2, HEIGHT // 2)]
    snake_direction = "RIGHT"
    snake_speed = 5
    # Reset food and score (but NOT high score)
    food = (random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE))
    score = 0
def draw_score():
    """Display the current score and high score at the top-left corner."""
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 40))
# Main game loop
running = True
while running:
    screen.fill(BLACK)
    draw_grid()
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != "DOWN":
                snake_direction = "UP"
            elif event.key == pygame.K_DOWN and snake_direction != "UP":
                snake_direction = "DOWN"
            elif event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                snake_direction = "LEFT"
            elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                snake_direction = "RIGHT"
   # Move Snake
    x, y = snake_body[0]  # Head position
    if snake_direction == "UP":
        y -= BLOCK_SIZE
    elif snake_direction == "DOWN":
        y += BLOCK_SIZE
    elif snake_direction == "LEFT":
        x -= BLOCK_SIZE
    elif snake_direction == "RIGHT":
        x += BLOCK_SIZE
    new_head = (x, y)
    # Collision Detection (Game Over)
    if new_head in snake_body or x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        if show_game_over():  # If Restart button is clicked
            restart_game()
            continue  # Skip rest of loop and restart immediately
    # Add new head to the body
    snake_body.insert(0, new_head)
    # Check if the snake eats food
    if new_head == food:
        food = (random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE))
        snake_speed += speed_increment
        score += 10
    else:
        # Remove last segment to keep the snake's length consistent
        snake_body.pop()
    # Draw everything
    draw_snake()
    pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
    draw_score()
    pygame.display.flip()
    clock.tick(snake_speed)
pygame.quit()