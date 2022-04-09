import gym
import gym_snake
import numpy as np
from snakeUtils import *
from operator import add, sub
from typing import Tuple

ACTIONS = {0: 'UP', 1: 'RIGHT', 2: 'DOWN', 3: 'LEFT'}


def node_add(node_a: Tuple[int, int], node_b: Tuple[int, int]):
    result: Tuple[int, int] = tuple(map(add, node_a, node_b))
    return result


def node_sub(node_a: Tuple[int, int], node_b: Tuple[int, int]):
    result: Tuple[int, int] = tuple(map(sub, node_a, node_b))
    return result


def heuristic(start, goal):
    return (start[0] - goal[0])**2 + (start[1] - goal[1])**2


def astar_path(food, snake, grid):
    came_from = {}
    close_list = set()
    goal = tuple(food)
    start = tuple(get_snake_pos(snake))
    neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    open_list = [(fscore[start], start)]
    #print(start, goal, open_list)
    while open_list:
        print(open_list)
        print("that was open_list")
        current = min(open_list, key=lambda x: x[0])[1]
        print(current)
        print("that was current")
        open_list.pop(0)
        #print(current)
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
                print(data)
            return data[-1]

        close_list.add(current)

        for neighbor in neighbors:
            neighbor_node = node_add(current, neighbor)

            if dead_checking(grid, neighbor_node) or neighbor_node in close_list:
                continue
            if sum(map(abs, node_sub(current, neighbor_node))) == 2:
                diff = node_sub(current, neighbor_node)
                if dead_checking(grid, node_add(neighbor_node, (0, diff[1]))
                                             ) or node_add(neighbor_node, (0, diff[1])) in close_list:
                    continue
                elif dead_checking(grid, node_add(neighbor_node, (diff[0], 0))
                                               ) or node_add(neighbor_node, (diff[0], 0)) in close_list:
                    continue
            tentative_gscore = gscore[current] + heuristic(current, neighbor_node)
            if tentative_gscore < gscore.get(neighbor_node, 0) or neighbor_node not in [i[1] for i in open_list]:
                gscore[neighbor_node] = tentative_gscore
                fscore[neighbor_node] = tentative_gscore + heuristic(neighbor_node, goal)
                open_list.append((fscore[neighbor_node], neighbor_node))
                came_from[neighbor_node] = current


if __name__ == "__main__":
    env = gym.make('snake-v0')
    env.render()
    state = env.reset()
    done = False
    game_controller = env.controller

    grid_object = game_controller.grid
    grid_pixels = grid_object.grid

    snakes_array = game_controller.snakes
    snake = snakes_array[0]
    obs = grid_pixels
    steps = 1
    total_pts = 0

    while not done:
        current = tuple(get_snake_pos(snake))
        target = astar_path(get_food_pos(obs), snake, grid_object)
        print("Step"+str(steps))
        print(current)
        print(target)
        print("rewards"+str(total_pts))
        action = get_action(current, target)
        print(ACTIONS[action])
        obs, rewards, done, info = env.step(action)
        print("----------")
        print("nextfood"+str(get_food_pos(obs)))
        total_pts = total_pts + rewards
        steps = steps + 1
        env.render()
