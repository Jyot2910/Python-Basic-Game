import pygame
import sys
import random

pygame.init()

# Screen
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BG_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)

# Clock
clock = pygame.time.Clock()
SPEED = 10

# Snake setup
snake = [(WIDTH//2, HEIGHT//2)]
dx, dy = 0, 0

# Food setup
def random_food():
    x = random.randint(0, COLS-1) * CELL_SIZE
    y = random.randint(0, ROWS-1) * CELL_SIZE
    while (x, y) in snake:
        x = random.randint(0, COLS-1) * CELL_SIZE
        y = random.randint(0, ROWS-1) * CELL_SIZE
    return (x, y)

food = random_food()

# Game over
def game_over():
    font = pygame.font.SysFont(None, 55)
    text = font.render("Game Over! Press R to Restart", True, (255, 255, 255))
    screen.blit(text, (20, HEIGHT//2 - 30))
    pygame.display.update()

# Restart game
def restart():
    global snake, dx, dy, food
    snake = [(WIDTH//2, HEIGHT//2)]
    dx, dy = 0, 0
    food = random_food()

# Main loop
running = True
gameover = False
while running:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -CELL_SIZE
            elif event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, CELL_SIZE
            elif event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -CELL_SIZE, 0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = CELL_SIZE, 0
            elif event.key == pygame.K_r and gameover:
                restart()
                gameover = False

    if not gameover:
        # Move snake
        head_x, head_y = snake[-1]
        new_head = (head_x + dx, head_y + dy)
        snake.append(new_head)

        # Check collision with walls
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT):
            gameover = True

        # Check collision with self
        if new_head in snake[:-1]:
            gameover = True

        # Check if food eaten
        if new_head == food:
            food = random_food()
        else:
            snake.pop(0)

    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, SNAKE_COLOR, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    # Draw food
    pygame.draw.rect(screen, FOOD_COLOR, (food[0], food[1], CELL_SIZE, CELL_SIZE))

    if gameover:
        game_over()

    pygame.display.update()
    clock.tick(SPEED)
