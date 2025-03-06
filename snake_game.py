import pygame
import sys
import random

# Initialize PyGame
pygame.init()

# Set window size to 720x600
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Two Snake Game')

# Color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initial position and size of snake and food
snake_block_size = 20
initial_snake_length = 5
initial_snake_speed = 8

# Generate random initial positions for two snakes in left and right areas
def generate_random_snake_pos(side):
    if side == 'left':
        start_x = random.randrange(1, (SCREEN_WIDTH // 2 // snake_block_size)) * snake_block_size
    else:
        start_x = random.randrange((SCREEN_WIDTH // 2 // snake_block_size) + 1, (SCREEN_WIDTH // snake_block_size)) * snake_block_size
    start_y = random.randrange(1, (SCREEN_HEIGHT // snake_block_size)) * snake_block_size
    direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
    snake_pos = []
    if direction == 'UP':
        for i in range(initial_snake_length):
            snake_pos.append([start_x, start_y + i * snake_block_size])
    elif direction == 'DOWN':
        for i in range(initial_snake_length):
            snake_pos.append([start_x, start_y - i * snake_block_size])
    elif direction == 'LEFT':
        for i in range(initial_snake_length):
            snake_pos.append([start_x + i * snake_block_size, start_y])
    elif direction == 'RIGHT':
        for i in range(initial_snake_length):
            snake_pos.append([start_x - i * snake_block_size, start_y])
    return snake_pos

snake1_pos = generate_random_snake_pos('left')
snake2_pos = generate_random_snake_pos('right')

snake1_speed = initial_snake_speed
snake2_speed = initial_snake_speed
food_pos = [random.randrange(1, (SCREEN_WIDTH // snake_block_size)) * snake_block_size, random.randrange(1, (SCREEN_HEIGHT // snake_block_size)) * snake_block_size]
food_spawn = True

def reset_game():
    global snake1_pos, snake2_pos, snake1_direction, snake2_direction, food_pos, food_spawn, game_over, snake1_speed, snake2_speed
    snake1_pos = generate_random_snake_pos('left')
    snake2_pos = generate_random_snake_pos('right')
    snake1_direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
    snake2_direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
    food_pos = [random.randrange(1, (SCREEN_WIDTH // snake_block_size)) * snake_block_size, random.randrange(1, (SCREEN_HEIGHT // snake_block_size)) * snake_block_size]
    food_spawn = True
    game_over = False
    snake1_speed = initial_snake_speed
    snake2_speed = initial_snake_speed

# 智能移动函数，增加避开另一条蛇、自己和边缘的逻辑
def intelligent_move(snake_pos, direction, food_pos, other_snake_pos, other_snake_direction):
    head_x, head_y = snake_pos[0]
    food_x, food_y = food_pos
    possible_directions = []

    new_positions = {
        'UP': [head_x, head_y - snake_block_size],
        'DOWN': [head_x, head_y + snake_block_size],
        'LEFT': [head_x - snake_block_size, head_y],
        'RIGHT': [head_x + snake_block_size, head_y]
    }

    other_head_x, other_head_y = other_snake_pos[0]
    if other_snake_direction == 'UP':
        other_next_pos = [other_head_x, other_head_y - snake_block_size]
    elif other_snake_direction == 'DOWN':
        other_next_pos = [other_head_x, other_head_y + snake_block_size]
    elif other_snake_direction == 'LEFT':
        other_next_pos = [other_head_x - snake_block_size, other_head_y]
    elif other_snake_direction == 'RIGHT':
        other_next_pos = [other_head_x + snake_block_size, other_head_y]

    my_distance = abs(head_x - food_x) + abs(head_y - food_y)
    other_distance = abs(other_head_x - food_x) + abs(other_head_y - food_y)

    if my_distance > other_distance:
        # 修改后的边界检查逻辑
        if head_x < SCREEN_WIDTH // 2 and direction != 'LEFT':
            if (new_positions['RIGHT'][0] + snake_block_size <= SCREEN_WIDTH and
                new_positions['RIGHT'] not in other_snake_pos and
                new_positions['RIGHT'] != other_next_pos and
                new_positions['RIGHT'] not in snake_pos[1:]):
                possible_directions.append('RIGHT')
        elif head_x > SCREEN_WIDTH // 2 and direction != 'RIGHT':
            if (new_positions['LEFT'][0] >= 0 and
                new_positions['LEFT'] not in other_snake_pos and
                new_positions['LEFT'] != other_next_pos and
                new_positions['LEFT'] not in snake_pos[1:]):
                possible_directions.append('LEFT')
        if not possible_directions:
            if head_y < SCREEN_HEIGHT // 2 and direction != 'UP':
                if (new_positions['DOWN'][1] + snake_block_size <= SCREEN_HEIGHT and
                    new_positions['DOWN'] not in other_snake_pos and
                    new_positions['DOWN'] != other_next_pos and
                    new_positions['DOWN'] not in snake_pos[1:]):
                    possible_directions.append('DOWN')
            elif head_y > SCREEN_HEIGHT // 2 and direction != 'DOWN':
                if (new_positions['UP'][1] >= 0 and
                    new_positions['UP'] not in other_snake_pos and
                    new_positions['UP'] != other_next_pos and
                    new_positions['UP'] not in snake_pos[1:]):
                    possible_directions.append('UP')
    else:
        # 正常追食物时的修改
        if head_x < food_x and direction != 'LEFT':
            if (new_positions['RIGHT'][0] + snake_block_size <= SCREEN_WIDTH and
                new_positions['RIGHT'] not in other_snake_pos and
                new_positions['RIGHT'] != other_next_pos and
                new_positions['RIGHT'] not in snake_pos[1:]):
                possible_directions.append('RIGHT')
        if head_x > food_x and direction != 'RIGHT':
            if (new_positions['LEFT'][0] >= 0 and
                new_positions['LEFT'] not in other_snake_pos and
                new_positions['LEFT'] != other_next_pos and
                new_positions['LEFT'] not in snake_pos[1:]):
                possible_directions.append('LEFT')
        if head_y < food_y and direction != 'UP':
            if (new_positions['DOWN'][1] + snake_block_size <= SCREEN_HEIGHT and
                new_positions['DOWN'] not in other_snake_pos and
                new_positions['DOWN'] != other_next_pos and
                new_positions['DOWN'] not in snake_pos[1:]):
                possible_directions.append('DOWN')
        if head_y > food_y and direction != 'DOWN':
            if (new_positions['UP'][1] >= 0 and
                new_positions['UP'] not in other_snake_pos and
                new_positions['UP'] != other_next_pos and
                new_positions['UP'] not in snake_pos[1:]):
                possible_directions.append('UP')

    if possible_directions:
        return random.choice(possible_directions)
    return direction

def main():
    global food_spawn, food_pos, game_over, snake1_speed, snake2_speed
    snake1_direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
    snake2_direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
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

        if not game_over:
            # 智能决定蛇的移动方向
            snake1_direction = intelligent_move(snake1_pos, snake1_direction, food_pos, snake2_pos, snake2_direction)
            snake2_direction = intelligent_move(snake2_pos, snake2_direction, food_pos, snake1_pos, snake2_direction)

            # Move snake 1 based on the current direction
            if snake1_direction == 'UP':
                new_head1 = [snake1_pos[0][0], snake1_pos[0][1] - snake_block_size]
            elif snake1_direction == 'DOWN':
                new_head1 = [snake1_pos[0][0], snake1_pos[0][1] + snake_block_size]
            elif snake1_direction == 'LEFT':
                new_head1 = [snake1_pos[0][0] - snake_block_size, snake1_pos[0][1]]
            elif snake1_direction == 'RIGHT':
                new_head1 = [snake1_pos[0][0] + snake_block_size, snake1_pos[0][1]]

            # Move snake 2 based on the current direction
            if snake2_direction == 'UP':
                new_head2 = [snake2_pos[0][0], snake2_pos[0][1] - snake_block_size]
            elif snake2_direction == 'DOWN':
                new_head2 = [snake2_pos[0][0], snake2_pos[0][1] + snake_block_size]
            elif snake2_direction == 'LEFT':
                new_head2 = [snake2_pos[0][0] - snake_block_size, snake2_pos[0][1]]
            elif snake2_direction == 'RIGHT':
                new_head2 = [snake2_pos[0][0] + snake_block_size, snake2_pos[0][1]]

            # Check if snake 1 has eaten the food
            snake1_rect = pygame.Rect(new_head1[0], new_head1[1], snake_block_size, snake_block_size)
            food_rect = pygame.Rect(food_pos[0], food_pos[1], snake_block_size, snake_block_size)
            if snake1_rect.colliderect(food_rect):
                food_spawn = False
                snake1_speed += 1  # Increase speed when the snake eats food
            else:
                snake1_pos.pop()  # Remove the last part of the snake unless it's eaten food

            snake1_pos.insert(0, new_head1)

            # Check if snake 2 has eaten the food
            snake2_rect = pygame.Rect(new_head2[0], new_head2[1], snake_block_size, snake_block_size)
            if snake2_rect.colliderect(food_rect):
                food_spawn = False
                snake2_speed += 1  # Increase speed when the snake eats food
            else:
                snake2_pos.pop()  # Remove the last part of the snake unless it's eaten food

            snake2_pos.insert(0, new_head2)

            # Spawn new food if necessary
            if not food_spawn:
                food_pos = [random.randrange(1, (SCREEN_WIDTH // snake_block_size)) * snake_block_size, random.randrange(1, (SCREEN_HEIGHT // snake_block_size)) * snake_block_size]
                food_spawn = True

            # Check for collision with the window edges
            if snake1_pos[0][0] < 0 or snake1_pos[0][0] >= SCREEN_WIDTH or snake1_pos[0][1] < 0 or snake1_pos[0][1] >= SCREEN_HEIGHT:
                game_over = True
                winner = 2
            if snake2_pos[0][0] < 0 or snake2_pos[0][0] >= SCREEN_WIDTH or snake2_pos[0][1] < 0 or snake2_pos[0][1] >= SCREEN_HEIGHT:
                game_over = True
                winner = 1

            # Check for collision with itself
            if new_head1 in snake1_pos[1:]:
                game_over = True
                winner = 2
            if new_head2 in snake2_pos[1:]:
                game_over = True
                winner = 1

            # Check for collision between snakes
            if new_head1 in snake2_pos or new_head2 in snake1_pos:
                game_over = True
                if len(snake1_pos) > len(snake2_pos):
                    winner = 1
                elif len(snake2_pos) > len(snake1_pos):
                    winner = 2
                else:
                    winner = 0  # Tie

            # Draw the game screen
            screen.fill(BLACK)
            for pos in snake1_pos:
                pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], snake_block_size, snake_block_size))
            for pos in snake2_pos:
                pygame.draw.rect(screen, BLUE, pygame.Rect(pos[0], pos[1], snake_block_size, snake_block_size))
            pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], snake_block_size, snake_block_size))

            # Display snake lengths at the top center
            font = pygame.font.Font(None, 36)
            length_text1 = font.render(f'Snake 1 Length: {len(snake1_pos)}', 1, WHITE)
            length_text2 = font.render(f'Snake 2 Length: {len(snake2_pos)}', 1, WHITE)
            screen.blit(length_text1, (SCREEN_WIDTH // 2 - length_text1.get_width() // 2, 10))
            screen.blit(length_text2, (SCREEN_WIDTH // 2 - length_text2.get_width() // 2, 50))

        else:
            screen.fill(BLACK)
            font = pygame.font.Font(None, 36)
            if winner == 0:
                text_lines = ["Game Over! It's a Tie!", "Press Enter to Restart or Esc to Quit."]
            else:
                text_lines = [f"Game Over! Snake {winner} Wins!", "Press Enter to Restart or Esc to Quit."]
            for i, line in enumerate(text_lines):
                text = font.render(line, 1, WHITE)
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 + i * 40))

        pygame.display.flip()
        clock.tick(max(snake1_speed, snake2_speed))

if __name__ == "__main__":
    main()