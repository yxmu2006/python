import pygame
import sys
import random

# 初始化 PyGame
pygame.init()

# 设置窗口大小
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Two Snake Game')

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 蛇和食物的大小及初始参数
snake_block_size = 20
initial_snake_length = 5
initial_snake_speed = 8

# 全局变量
snake1_pos = []
snake2_pos = []
food_pos = []
snake1_direction = ''
snake2_direction = ''
food_spawn = True
game_over = False
snake1_speed = initial_snake_speed
snake2_speed = initial_snake_speed

# 生成随机初始蛇位置
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

# 重置游戏函数
def reset_game():
    global snake1_pos, snake2_pos, snake1_direction, snake2_direction, food_pos, food_spawn, game_over, snake1_speed, snake2_speed
    snake1_pos = generate_random_snake_pos('left')
    snake2_pos = generate_random_snake_pos('right')
    snake1_direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
    snake2_direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
    while True:
        food_pos = [random.randrange(1, (SCREEN_WIDTH // snake_block_size)) * snake_block_size, 
                    random.randrange(1, (SCREEN_HEIGHT // snake_block_size)) * snake_block_size]
        if food_pos not in snake1_pos and food_pos not in snake2_pos:
            break
    food_spawn = True
    game_over = False
    snake1_speed = initial_snake_speed
    snake2_speed = initial_snake_speed

# 改进的智能移动函数
def intelligent_move(snake_pos, direction, food_pos, other_snake_pos):
    head_x, head_y = snake_pos[0]
    food_x, food_y = food_pos
    
    # 计算所有可能的新位置
    new_positions = {
        'UP': [head_x, head_y - snake_block_size],
        'DOWN': [head_x, head_y + snake_block_size],
        'LEFT': [head_x - snake_block_size, head_y],
        'RIGHT': [head_x + snake_block_size, head_y]
    }
    
    # 首先确定安全方向
    safe_directions = []
    for d in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
        new_pos = new_positions[d]
        if (0 <= new_pos[0] < SCREEN_WIDTH and 
            0 <= new_pos[1] < SCREEN_HEIGHT and
            new_pos not in snake_pos[1:] and 
            new_pos not in other_snake_pos):
            safe_directions.append(d)
    
    # 如果有安全方向，则从中选择最佳方向
    if safe_directions:
        best_direction = None
        min_distance = float('inf')
        for d in safe_directions:
            new_pos = new_positions[d]
            distance = abs(new_pos[0] - food_x) + abs(new_pos[1] - food_y)
            if distance < min_distance:
                min_distance = distance
                best_direction = d
        return best_direction if best_direction else random.choice(safe_directions)
    # 如果没有安全方向，保持当前方向
    return direction

# 主游戏循环
def main():
    global food_pos, snake1_pos, snake2_pos, snake1_direction, snake2_direction, food_spawn, game_over, snake1_speed, snake2_speed
    reset_game()  # 确保游戏开始时重置所有变量
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_RETURN:
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if not game_over:
            # AI控制移动
            snake1_direction = intelligent_move(snake1_pos, snake1_direction, food_pos, snake2_pos)
            snake2_direction = intelligent_move(snake2_pos, snake2_direction, food_pos, snake1_pos)

            # 计算新头部位置
            new_head1 = list(snake1_pos[0])
            if snake1_direction == 'UP':
                new_head1[1] -= snake_block_size
            elif snake1_direction == 'DOWN':
                new_head1[1] += snake_block_size
            elif snake1_direction == 'LEFT':
                new_head1[0] -= snake_block_size
            elif snake1_direction == 'RIGHT':
                new_head1[0] += snake_block_size

            new_head2 = list(snake2_pos[0])
            if snake2_direction == 'UP':
                new_head2[1] -= snake_block_size
            elif snake2_direction == 'DOWN':
                new_head2[1] += snake_block_size
            elif snake2_direction == 'LEFT':
                new_head2[0] -= snake_block_size
            elif snake2_direction == 'RIGHT':
                new_head2[0] += snake_block_size

            # 检查是否吃到食物
            snake1_rect = pygame.Rect(new_head1[0], new_head1[1], snake_block_size, snake_block_size)
            snake2_rect = pygame.Rect(new_head2[0], new_head2[1], snake_block_size, snake_block_size)
            food_rect = pygame.Rect(food_pos[0], food_pos[1], snake_block_size, snake_block_size)

            if snake1_rect.colliderect(food_rect):
                food_spawn = False
                snake1_speed += 1
            else:
                snake1_pos.pop()
            snake1_pos.insert(0, new_head1)

            if snake2_rect.colliderect(food_rect):
                food_spawn = False
                snake2_speed += 1
            else:
                snake2_pos.pop()
            snake2_pos.insert(0, new_head2)

            # 生成新食物，确保不与蛇身重叠
            if not food_spawn:
                while True:
                    food_pos = [random.randrange(1, (SCREEN_WIDTH // snake_block_size)) * snake_block_size, 
                                random.randrange(1, (SCREEN_HEIGHT // snake_block_size)) * snake_block_size]
                    if food_pos not in snake1_pos and food_pos not in snake2_pos:
                        break
                food_spawn = True

            # 检查碰撞
            if (snake1_pos[0][0] < 0 or snake1_pos[0][0] >= SCREEN_WIDTH or 
                snake1_pos[0][1] < 0 or snake1_pos[0][1] >= SCREEN_HEIGHT or 
                new_head1 in snake1_pos[1:]):
                game_over = True
                winner = 2
            if (snake2_pos[0][0] < 0 or snake2_pos[0][0] >= SCREEN_WIDTH or 
                snake2_pos[0][1] < 0 or snake2_pos[0][1] >= SCREEN_HEIGHT or 
                new_head2 in snake2_pos[1:]):
                game_over = True
                winner = 1

            # 检查蛇之间的碰撞，包括头对头
            if new_head1 in snake2_pos or new_head2 in snake1_pos or new_head1 == new_head2:
                game_over = True
                if new_head1 == new_head2:
                    winner = 0  # 头对头碰撞，平局
                elif len(snake1_pos) > len(snake2_pos):
                    winner = 1
                elif len(snake2_pos) > len(snake1_pos):
                    winner = 2
                else:
                    winner = 0

            # 绘制游戏画面
            screen.fill(BLACK)
            for pos in snake1_pos:
                pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], snake_block_size, snake_block_size))
            for pos in snake2_pos:
                pygame.draw.rect(screen, BLUE, pygame.Rect(pos[0], pos[1], snake_block_size, snake_block_size))
            pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], snake_block_size, snake_block_size))

            # 显示蛇的长度
            font = pygame.font.Font(None, 36)
            length_text1 = font.render(f'Snake 1 Length: {len(snake1_pos)}', 1, WHITE)
            length_text2 = font.render(f'Snake 2 Length: {len(snake2_pos)}', 1, WHITE)
            screen.blit(length_text1, (SCREEN_WIDTH // 2 - length_text1.get_width() // 2, 10))
            screen.blit(length_text2, (SCREEN_WIDTH // 2 - length_text2.get_width() // 2, 50))

        else:
            screen.fill(BLACK)
            font = pygame.font.Font(None, 36)
            text_lines = ["Game Over! It's a Tie!", "Press Enter to Restart or Esc to Quit."] if winner == 0 else \
                         [f"Game Over! Snake {winner} Wins!", "Press Enter to Restart or Esc to Quit."]
            for i, line in enumerate(text_lines):
                text = font.render(line, 1, WHITE)
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 + i * 40))

        pygame.display.flip()
        clock.tick(max(snake1_speed, snake2_speed))

if __name__ == "__main__":
    main()