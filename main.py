import pygame
import random
import sys
import time
from pygame.locals import *
from collections import deque

SCREEN_WIDTH = 600  #屏幕宽度
SCREEN_HEIGHT = 480 #屏幕高度
SIZE = 20       #小方格大小
LINE_WIDTH = 1  #网格线宽度

#游戏区域坐标范围
SCOPE_X = (0,SCREEN_WIDTH//SIZE - 1)
SCOPE_Y = (2,SCREEN_HEIGHT//SIZE - 1)

#小球的分值和颜色
BALL_STYLE_LIST = [(10,(255,100,100)), (20,(100,255,100)), (30,(100,100,255))]

#布局颜色
LIGHT = (100,100,100)
DARK = (200,200,200)
BLACK = (0,0,0)
RED = (200,30,30)
BACKGROUND_COLOR = (40,40,60)


def print_text(screen, font, x, y, text, font_color = (255,255,255)):
    img_text = font.render(text,True,font_color)
    screen.blit(img_text, (x,y))
def init_snake():
    snake = deque()
    snake.append((2,SCOPE_Y[0]))
    snake.append((1,SCOPE_Y[0]))
    snake.append((0,SCOPE_Y[0]))
    return snake

def create_ball(snake):
    ball_x = random.randint(SCOPE_X[0],SCOPE_X[1])
    ball_y = random.randint(SCOPE_Y[0],SCOPE_Y[1])
    while((ball_x,ball_y)) in snake:
        ball_x = random.randint(SCOPE_X[0], SCOPE_X[1])
        ball_y = random.randint(SCOPE_Y[0], SCOPE_Y[1])
    return ball_x,ball_y

def get_ball_style():
    return  BALL_STYLE_LIST[random.randint(0,2)]

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Gluttonous Snake")

    font1 = pygame.font.SysFont('SimHei', 24)   #得分字体
    font2 = pygame.font.Font(None,72)       #Game Over字体
    font_width, font_height = font2.size("Game Over")

    b = True

    snake = init_snake()
    ball = create_ball(snake)
    ball_style = get_ball_style()

    #方向
    position = (1,0)
    game_over = True
    start = False
    score = 0
    original_speed = 0.5
    speed = original_speed
    last_move_time = None
    pause = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if game_over == True:
                        start = True
                        game_over = False
                        b = True
                        snake = init_snake()
                        ball = create_ball(snake)
                        ball_style = get_ball_style()
                        position = (1,0)
                        score = 0
                        last_move_time = time.time()
                elif event.key == K_SPACE:
                    if not game_over:
                        pause = not pause
                elif event.key in (K_w, K_UP):
                    if b and not position[1]:
                        position = (0,-1)
                        b = False
                elif event.key in (K_s, K_DOWN):
                    if b and not position[1]:
                        position = (0,1)
                        b = False
                elif event.key in (K_a, K_LEFT):
                    if b and not position[0]:
                        position = (-1,0)
                        b = False
                elif event.key in (K_d, K_RIGHT):
                    if b and not position[0]:
                        position = (1,0)
                        b = False


        #填充颜色
        screen.fill(BACKGROUND_COLOR)
        #画网格
        for x in range(SIZE,SCREEN_WIDTH, SIZE):
            pygame.draw.line(screen,BLACK,(x,SCOPE_Y[0] * SIZE), (x,SCREEN_HEIGHT), LINE_WIDTH)
        for y in range(SCOPE_Y[0] * SIZE, SCREEN_HEIGHT, SIZE):
            pygame.draw.line(screen,BLACK,(0,y), (SCREEN_WIDTH,y), LINE_WIDTH)

        if not game_over:
            current_time = time.time()
            if current_time - last_move_time > speed:
                if not pause:
                    b = True
                    last_move_time = current_time
                    next_s = (snake[0][0] + position[0], snake[0][1] + position[1])
                    if next_s == ball:
                        snake.appendleft(next_s)
                        score += ball_style[0]
                        speed = original_speed - 0.03 * (score//100)
                        ball = create_ball(snake)
                        ball_style = get_ball_style()
                    else:
                        if SCOPE_X[0] <= next_s[0] <= SCOPE_X[1] and SCOPE_Y[0] <= next_s[1] <= SCOPE_Y[1] \
                                and next_s not in snake:
                            snake.appendleft(next_s)
                            snake.pop()
                        else:
                            game_over = True

        #画球
        if not game_over:
            pygame.draw.rect(screen, ball_style[1], (ball[0] * SIZE, ball[1] * SIZE, SIZE, SIZE), 0)

        #画蛇
        for s in snake:
            pygame.draw.rect(screen, DARK, (s[0] * SIZE + LINE_WIDTH, s[1] * SIZE + LINE_WIDTH, SIZE - LINE_WIDTH * 2\
                                            , SIZE - LINE_WIDTH * 2), 0)

        print_text(screen, font1, 30, 7, f'速度：{score // 100}')
        print_text(screen, font1, 450, 7, f'得分：{score}')

        if game_over:
            if start:
                print_text(screen, font2, (SCREEN_WIDTH - font_width) // 2, (SCREEN_HEIGHT - font_height) // 2, \
                           "Game Over", RED)

        pygame.display.update()




if __name__ == '__main__':
    main()