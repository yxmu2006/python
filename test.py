import pygame
import sys
import random

# Initialize PyGame
pygame.init()

# Set window size to 512x512
SCREEN_WIDTH, SCREEN_HEIGHT = 512, 512
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# Color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 1)

# Initial position and size of snake and food
snake_pos = [[256, 256], [246, 256], [236, 256]]  # Adjusted initial position to center
snake_speed = 10
food_pos = [random.randrange(1, (SCREEN_WIDTH//20)) * 20, random.randrange(1, (SCREEN_HEIGHT//20)) * 20]
food_spawn = True

def game_over():
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over! Press ENTER to restart.", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

def main():
    global food_spawn, food_pos
    direction = 'RIGHT'
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'

        # Move the snake based on the current direction
        if direction == 'UP':
            new_head = [snake_pos[0][0], snake_pos[0][1] - 20]
        elif direction == 'DOWN':
            new_head = [snake_pos[0][0], snake_pos[0][1] + 20]
        elif direction == 'LEFT':
            new_head = [snake_pos[0][0] - 20, snake_pos[0][1]]
        elif direction == 'RIGHT':
            new_head = [snake_pos[0][0] + 20, snake_pos[0][1]]

        # Check if the snake has hit the game window's edge
        if (new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH) or (new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT):
            game_over()
            # Reset the game state here if needed
            snake_pos = [[256, 256], [246, 256], [236, 256]]  # reset snake position
            direction = 'RIGHT'  # reset snake direction
            food_spawn = True   # force a new food spawn
            food_pos = [random.randrange(1, (SCREEN_WIDTH//20)) * 20, random.randrange(1, (SCREEN_HEIGHT//20)) * 20]  # generate a new food position
        else:
            snake_pos.insert(0, new_head)
            if not food_spawn:
                food_pos = [random.randrange(1, (SCREEN_WIDTH//20)) * 20, random.randrange(1, (SCREEN_HEIGHT//20)) * 20]
                food_spawn = True
            else:
                snake_pos.pop()  # Remove the last part of the snake unless it's eaten food

        # Draw the game screen
        screen.fill(BLACK)
        for pos in snake_pos:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 20, 20))
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], 20, 20))

        pygame.display.flip()
        clock.tick(snake_speed)


if __name__ == "__main__":
   main()
