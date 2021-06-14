from sys import exit

import pygame

from Constants import *
from Snake import Snake


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

looping = False
while True:
    cantBe = get_opposite(snake.get_head_dir())
    while looping:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
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
            if event.type == pygame.USEREVENT:
                looping = False
    pygame.time.set_timer(pygame.USEREVENT, 500)
    looping = True

    if not snake.iterate():
        print("Game Over!")
        exit()

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (200, 0, 0),
                     (snake.food.pos.x * SEGMENT_SIZE + 1,
                      SCREEN_SIZE[1] - (snake.food.pos.y * SEGMENT_SIZE - 1) - SEGMENT_SIZE,
                      SEGMENT_SIZE - 2, SEGMENT_SIZE - 2), 0)
    for i in snake.body:
        pygame.draw.rect(screen, (0, 200, 0),
                         (i.pos.x * SEGMENT_SIZE + 1,
                          SCREEN_SIZE[1] - (i.pos.y * SEGMENT_SIZE - 1) - SEGMENT_SIZE,
                          SEGMENT_SIZE - 2, SEGMENT_SIZE - 2), 0)

    pygame.display.flip()
    # print(snake.body[0].pos, snake.food.pos)

    elapsed_time = clock.tick()
