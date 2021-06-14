from sys import exit

import pygame

from Constants import *
from Snake import Snake
from SnakeAI import get_fastest_path


def get_opposite(direction):
    if direction == DIR.UP:
        return DIR.DOWN
    if direction == DIR.DOWN:
        return DIR.UP
    if direction == DIR.LEFT:
        return DIR.RIGHT
    if direction == DIR.RIGHT:
        return DIR.LEFT
    return DIR.NONE


snake = Snake()

__author__ = 'michaelschuff'
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
pygame.display.set_caption(CAPTION)
pygame.init()
clock = pygame.time.Clock()
elapsed_time = clock.tick()

path = []
path_index = 0

looping = False
while True:
    cantBe = get_opposite(snake.get_head_dir())
    while looping:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.USEREVENT:
                looping = False
            if USER_CONTROLLED:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if DIR.UP != cantBe:
                            snake.update_head_dir(DIR.UP)
                    elif event.key == pygame.K_DOWN:
                        if DIR.DOWN != cantBe:
                            snake.update_head_dir(DIR.DOWN)
                    elif event.key == pygame.K_LEFT:
                        if DIR.LEFT != cantBe:
                            snake.update_head_dir(DIR.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        if DIR.RIGHT != cantBe:
                            snake.update_head_dir(DIR.RIGHT)

    pygame.time.set_timer(pygame.USEREVENT, MILLISECONDS_PER_FRAME)
    looping = True

    if not USER_CONTROLLED:
        if snake.didEat or path_index == len(path):
            path = get_fastest_path(snake)
            path_index = 0
        snake.update_head_dir(path[path_index])
        path_index += 1

    if not snake.iterate():
        print("Game Over!")
        pygame.quit()
        exit()

    screen.fill((0, 0, 0))

    # draw Food
    pygame.draw.rect(screen, (200, 0, 0),
                     (snake.food.pos.x * SEGMENT_SIZE + 1,
                      SCREEN_SIZE[1] - (snake.food.pos.y * SEGMENT_SIZE - 1) - SEGMENT_SIZE,
                      SEGMENT_SIZE - 2, SEGMENT_SIZE - 2), 0)

    # draw Segments
    for i in range(len(snake.body) - 1):
        x = snake.body[i].pos.x * SEGMENT_SIZE
        y = SCREEN_SIZE[1] - snake.body[i].pos.y * SEGMENT_SIZE - SEGMENT_SIZE
        pygame.draw.rect(screen, (0, 200, 0), (x + 1, y + 1, SEGMENT_SIZE - 2, SEGMENT_SIZE - 2), 0)

        if snake.body[i + 1].dir == DIR.UP:
            pygame.draw.rect(screen, (0, 200, 0), (x + 1, y + SEGMENT_SIZE - 1, SEGMENT_SIZE - 2, 2), 0)
        if snake.body[i + 1].dir == DIR.DOWN:
            pygame.draw.rect(screen, (0, 200, 0), (x + 1, y - 1, SEGMENT_SIZE - 2, 2), 0)
        if snake.body[i + 1].dir == DIR.LEFT:
            pygame.draw.rect(screen, (0, 200, 0), (x + SEGMENT_SIZE - 1, y + 1, 2, SEGMENT_SIZE - 2), 0)
        if snake.body[i + 1].dir == DIR.RIGHT:
            pygame.draw.rect(screen, (0, 200, 0), (x - 1, y + 1, 2, SEGMENT_SIZE - 2), 0)

    # draw last segment
    x = snake.body[len(snake.body) - 1].pos.x * SEGMENT_SIZE
    y = SCREEN_SIZE[1] - snake.body[len(snake.body) - 1].pos.y * SEGMENT_SIZE - SEGMENT_SIZE
    pygame.draw.rect(screen, (0, 200, 0), (x + 1, y + 1, SEGMENT_SIZE - 2, SEGMENT_SIZE - 2), 0)

    pygame.display.update()

    elapsed_time = clock.tick()
