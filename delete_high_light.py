import pygame
import sys
import random

# 初始化pygame
pygame.init()

# 设置窗口大小，这里可以调整为1024x1024
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 蛇和食物的初始位置及尺寸
snake_pos = [[300, 300], [290, 300], [280, 300]]
snake_speed = 10
food_pos = [random.randrange(1, (SCREEN_WIDTH//10)) * 10, random.randrange(1, (SCREEN_HEIGHT//10)) * 10]
food_spawn = True

# 游戏主循环
def main():
    global food_spawn
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

        # 根据方向移动蛇
        if direction == 'UP':
            snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1] - 10])
        elif direction == 'DOWN':
            snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1] + 10])
        elif direction == 'LEFT':
            snake_pos.insert(0, [snake_pos[0][0] - 10, snake_pos[0][1]])
        elif direction == 'RIGHT':
            snake_pos.insert(0, [snake_pos[0][0] + 10, snake_pos[0][1]])

        # 检查是否吃到食物
        if snake_pos[0] == food_pos:
            food_spawn = False
        else:
            snake_pos.pop()

        # 如果没吃到食物，重新生成食物
        if not food_spawn:
            food_pos = [random.randrange(1, (SCREEN_WIDTH//10)) * 10, random.randrange(1, (SCREEN_HEIGHT//10)) * 10]
            food_spawn = True
        
        # 绘制界面
        screen.fill(BLACK)
        for pos in snake_pos:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        pygame.display.flip()
        clock.tick(snake_speed)

if __name__ == "__main__":
    main()