import pygame
import sys
import random

# Initialize PyGame
pygame.init()

# Set window size to 720x600
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# Color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initial position and size of snake and food
snake_block_size = 20
snake_pos = [[360, 360], [340, 360], [320, 360]]  # Adjusted initial position to center
initial_snake_speed = 8
snake_speed = initial_snake_speed
food_pos = [random.randrange(1, (SCREEN_WIDTH // snake_block_size)) * snake_block_size, random.randrange(1, (SCREEN_HEIGHT // snake_block_size)) * snake_block_size]
food_spawn = True

def reset_game():
    global snake_pos, direction, food_pos, food_spawn, game_over, snake_speed
    snake_pos = [[360, 360], [340, 360], [320, 360]]  # Reset snake position
    direction = 'RIGHT'
    food_pos = [random.randrange(1, (SCREEN_WIDTH // snake_block_size)) * snake_block_size, random.randrange(1, (SCREEN_HEIGHT // snake_block_size)) * snake_block_size]
    food_spawn = True
    game_over = False
    snake_speed = initial_snake_speed  # Reset snake speed

def main():
    global food_spawn, food_pos, game_over, snake_speed
    direction = 'RIGHT'
    clock = pygame.time.Clock()
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_RETURN:
                        reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                else:
                    if event.key == pygame.K_UP and direction != 'DOWN':
                        direction = 'UP'
                    elif event.key == pygame.K_DOWN and direction != 'UP':
                        direction = 'DOWN'
                    elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                        direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                        direction = 'RIGHT'

        if not game_over:
            # Move the snake based on the current direction
            if direction == 'UP':
                new_head = [snake_pos[0][0], snake_pos[0][1] - snake_block_size]
            elif direction == 'DOWN':
                new_head = [snake_pos[0][0], snake_pos[0][1] + snake_block_size]
            elif direction == 'LEFT':
                new_head = [snake_pos[0][0] - snake_block_size, snake_pos[0][1]]
            elif direction == 'RIGHT':
                new_head = [snake_pos[0][0] + snake_block_size, snake_pos[0][1]]

            # Check if the snake has eaten the food
            snake_rect = pygame.Rect(new_head[0], new_head[1], snake_block_size, snake_block_size)
            food_rect = pygame.Rect(food_pos[0], food_pos[1], snake_block_size, snake_block_size)
            if snake_rect.colliderect(food_rect):
                food_spawn = False
                snake_speed += 1  # Increase speed when the snake eats food
            else:
                snake_pos.pop()  # Remove the last part of the snake unless it's eaten food

            snake_pos.insert(0, new_head)

            # Spawn new food if necessary
            if not food_spawn:
                food_pos = [random.randrange(1, (SCREEN_WIDTH // snake_block_size)) * snake_block_size, random.randrange(1, (SCREEN_HEIGHT // snake_block_size)) * snake_block_size]
                food_spawn = True

            # Check for collision with the window edges
            if snake_pos[0][0] < 0 or snake_pos[0][0] >= SCREEN_WIDTH or snake_pos[0][1] < 0 or snake_pos[0][1] >= SCREEN_HEIGHT:
                game_over = True

            # Check for collision with itself
            if new_head in snake_pos[1:]:
                game_over = False

            # Draw the game screen
            screen.fill(BLACK)
            for pos in snake_pos:
                pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], snake_block_size, snake_block_size))
            pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], snake_block_size, snake_block_size))
            
            # Display snake length at the top center
            font = pygame.font.Font(None, 36)
            length_text = font.render(f'Snake Length: {len(snake_pos)} snake_speed:{snake_speed}', 1, WHITE)
            screen.blit(length_text, (SCREEN_WIDTH // 2 - length_text.get_width() // 2, 10))  # Position at top with 10px padding
        
        else:
            screen.fill(BLACK)
            font = pygame.font.Font(None, 36)
            text_lines = ["Game Over!", "Press Enter to Restart or Esc to Quit."]
            for i, line in enumerate(text_lines):
                text = font.render(line, 1, WHITE)
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 + i * 40))
            
            # Display final snake length in the center
            length_text = font.render(f'Snake Length: {len(snake_pos)}', 1, WHITE)
            screen.blit(length_text, (SCREEN_WIDTH // 2 - length_text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 + 80))

        pygame.display.flip()
        clock.tick(snake_speed)

if __name__ == "__main__":
    main()
