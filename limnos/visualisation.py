"""
Visualization of routes
"""
from .types import Route, Maze

import matplotlib.pyplot as plt


def plot_route(route: Route) -> None:

    fig, ax = plt.subplots()

    for this_point, next_point in zip(route[:-1], route[1:]):
        xs = (this_point[0], next_point[0])
        ys = (this_point[1], next_point[1])
        ax.plot(xs, ys, 'b-o')

    plt.show()


def plot_maze(maze: Maze, show_route: bool=True) -> None:

    route = maze[0]
    walls = maze[1]

    fig, ax = plt.subplots()

    if show_route:
        for this_point, next_point in zip(route[:-1], route[1:]):
            xs = (this_point[0], next_point[0])
            ys = (this_point[1], next_point[1])
            ax.plot(xs, ys, color="#d6f5e3")

    for wall in walls:
        xs = (wall[0][0], wall[1][0])
        ys = (wall[0][1], wall[1][1])

        ax.plot(xs, ys, 'k', linewidth=2)

    plt.show()
