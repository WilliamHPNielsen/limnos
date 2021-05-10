"""
Visualization of routes
"""
from typing import Generator

from .types import Route, Routes, Maze, Trails

import matplotlib.pyplot as plt

ColorCode = str

ROUTE_COLOR = "#b0aaa3"
ROUTE_COLORS: list[ColorCode] = [
    "#89fb89",
    "#feff8f",
    "#ffb162",
    "#07b8b4",
    "#a33800"]


def color_picker(colors: list[ColorCode]) -> Generator[ColorCode, None, None]:
    """
    Generator that yields colors
    """
    n = 0
    while True:
        yield colors[n]
        n = (n + 1) % len(colors)


def plot_route(route: Route) -> None:

    fig, ax = plt.subplots()

    for this_point, next_point in zip(route[:-1], route[1:]):
        xs = (this_point[0], next_point[0])
        ys = (this_point[1], next_point[1])
        ax.plot(xs, ys, '-o', color=ROUTE_COLOR)

    plt.show()


def plot_routes(routes: Routes) -> None:

    fig, ax = plt.subplots()

    for route in routes:

        for this_point, next_point in zip(route[:-1], route[1:]):
            xs = (this_point[0], next_point[0])
            ys = (this_point[1], next_point[1])
            ax.plot(xs, ys, '-o', color=ROUTE_COLOR)

    plt.show()


def plot_trails(trails: Trails, color_coding: bool=False) -> None:
    """
    Plot a collection of trails
    """

    if color_coding:
        cp = color_picker(ROUTE_COLORS)
    else:
        cp = color_picker([ROUTE_COLOR])

    fig, ax = plt.subplots()

    for route in trails.all_routes():

        route_color = next(cp)

        for this_point, next_point in zip(route[:-1], route[1:]):
            xs = (this_point[0], next_point[0])
            ys = (this_point[1], next_point[1])
            ax.plot(xs, ys, '-o', color=route_color)

    plt.show()


def plot_maze(maze: Maze, show_route: bool=True) -> None:

    route = maze[0]
    walls = maze[1]

    fig, ax = plt.subplots()

    if show_route:
        for this_point, next_point in zip(route[:-1], route[1:]):
            xs = (this_point[0], next_point[0])
            ys = (this_point[1], next_point[1])
            ax.plot(xs, ys, color=ROUTE_COLOR)

    for wall in walls:
        xs = (wall[0][0], wall[1][0])
        ys = (wall[0][1], wall[1][1])

        ax.plot(xs, ys, 'k', linewidth=2)

    plt.show()
