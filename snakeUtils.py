import gym
import gym_snake
import numpy as np

ACTIONS = {0: 'UP', 1: 'RIGHT', 2: 'DOWN', 3: 'LEFT'}
BODY_COLOR = np.array([1,0,0], dtype=np.uint8)
HEAD_COLOR = np.array([255, 0, 0], dtype=np.uint8)
FOOD_COLOR = np.array([0,0,255], dtype=np.uint8)
SPACE_COLOR = np.array([0,255,0], dtype=np.uint8)
GRID_UNIT_SIZE = 10


def get_food_pos(grid):
    x = np.where((grid == FOOD_COLOR).all(axis=2))
    return [x[1][0] // GRID_UNIT_SIZE, x[0][0] // GRID_UNIT_SIZE]


def get_snake_direction(snake):
    return snake.direction


def get_snake_pos(snake):
    return snake.head


def get_snake_body(snake):
    return snake.body


def get_action(current, target):
    if target[0] > current[0]:
        return 1
    if target[0] < current[0]:
        return 3
    if target[1] < current[1]:
        return 0
    if target[1] > current[1]:
        return 2


def dead_checking(grid, coord):
    return grid.off_grid(coord) or grid.snake_space(coord)
