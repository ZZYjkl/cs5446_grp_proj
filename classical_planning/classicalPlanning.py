import gym
import gym_snake
from snakeUtils import *
from operator import add, sub
from typing import Tuple
import random

ACTIONS = {0: 'UP', 1: 'RIGHT', 2: 'DOWN', 3: 'LEFT'}


def node_add(node_a: Tuple[int, int], node_b: Tuple[int, int]):
    result: Tuple[int, int] = tuple(map(add, node_a, node_b))
    return result


def node_sub(node_a: Tuple[int, int], node_b: Tuple[int, int]):
    result: Tuple[int, int] = tuple(map(sub, node_a, node_b))
    return result


def heuristic(start, goal):
    return (start[0] - goal[0])**2 + (start[1] - goal[1])**2


def get_neighbors(node):
    for diff in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        yield node_add(node, diff)


def bfs_path(food, start, grid):
    queue = [[start]]

    while queue:
        path = queue[0]
        future_head = path[-1]

        if future_head == tuple(food):
            return path

        for next_node in get_neighbors(future_head):
            if dead_checking(grid, next_node) or any(next_node in sublist for sublist in queue):
                continue
            new_path = list(path)
            new_path.append(next_node)
            queue.append(new_path)

        queue.pop(0)


def astar_path(food, start, grid):
    came_from = {}
    close_list = set()
    goal = tuple(food)
    neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    open_list = [(fscore[start], start)]
    while open_list:
        current = min(open_list, key=lambda x: x[0])[1]
        open_list.pop(0)
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            if bfs_path(food, data[-1], grid):
                # return this value only if bfs doesnt indicate any dead end with this path
                return data[-1]
            else:
                continue

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
    algo_used = ''
    pts_list = []

    while not done:
        current = tuple(get_snake_pos(snake))
        target = astar_path(get_food_pos(obs), current, grid_object)
        algo_used = 'a-star'
        if not target:
            bfs_res = bfs_path(get_food_pos(obs), current, grid_object)
            if bfs_res:
                target = bfs_res[1]
                algo_used = 'bfs'
        print("Step #" + str(steps))
        print("Food: " + str(get_food_pos(obs)))
        print("Current position: " + str(current))
        if target:
            action = get_action(current, target)
        else:
            # just in case both algos return null
            action = random.choice(range(0, 3))
            algo_used = 'random'
        print("Recommended action: " + str(ACTIONS[action]))
        print("Algo used: " + str(algo_used))
        obs, rewards, done, info = env.step(action)
        total_pts = total_pts + rewards
        pts_list.append(total_pts)
        print("Points: " + str(total_pts))
        print("----------")
        steps = steps + 1
        env.render()

    print(pts_list)
