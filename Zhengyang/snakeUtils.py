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