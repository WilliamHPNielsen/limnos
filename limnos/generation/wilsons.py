"""
Module to generate mazes by Wilson's algorithm
Algorithm described eg by Wikipedia: https://en.wikipedia.org/wiki/Maze_generation_algorithm
    and visualised here: https://bl.ocks.org/mbostock/11357811
"""
from random import randint, choice
from typing import Optional, cast

import numpy as np

from limnos.types import (Point,
                          Route,
                          Trails,
                          add_points)


def _random_direction(n: int, m: int, p: Point) -> Point:
    if p[0] == 1:
        if p[1] == 1:
            r = choice([(2, 0), (0, 2)])
        elif p[1] == 2*m - 1:
            r = choice([(2, 0), (0, -2)])
        else:
            r = choice([(2, 0), (0, -2), (0, 2)])
    elif p[0] == 2*n - 1:
        if p[1] == 1:
            r = choice([(-2, 0), (0, 2)])
        elif p[1] == 2*m - 1:
            r = choice([(-2, 0), (0, -2)])
        else:
            r = choice([(-2, 0), (0, -2), (0, 2)])
    else:
        if p[1] == 1:
            r = choice([(-2, 0), (2, 0), (0, 2)])
        elif p[1] == 2*m - 1:
            r = choice([(-2, 0), (2, 0), (0, -2)])
        else:
            r = choice([(-2, 0), (2, 0), (0, -2), (0, 2)])

    return add_points(p, r)


def _loop_erased_random_walk(n: int, m: int, start: Point, end: Trails) -> Route:
    """
    Walks from `start` and ends in any point in `end`.
    Erases any loop formed with self by backtracking.
    The last point in this route is also in trails, so only use
    answer[:-1] if you are updating an existing trail
    """
    route: Route = [start]
    while not end.point_in_trails(route[-1]):
        next_point = _random_direction(n, m, route[-1])
        if len(route) > 1 and next_point == route[-2]:  # what a half-assed solution ...
            continue
        elif next_point in route:
            while route[-1] != next_point:
                route.pop()
        else:
            route.append(next_point)

    return route


def trails_generator(N: int, M: int) -> Trails:
    """
    Full trail generation, generates N x M system
    """
    all_free_points: set[Point] = set(
        [(2*n + 1, 2*m + 1) for n in range(N) for m in range(M)])

    # Cells are chosen arbitrarily, so I chose the start and end to begin with
    # so I know this is the solution already.
    start_cell: Point = 1, 1
    end_cell: Point = 2*N - 1, 2*M - 1
    solution_route = _loop_erased_random_walk(N, M, start_cell,
                                              Trails(main=Route((end_cell,)), branches=[]))

    all_free_points.difference_update(set(solution_route))

    trails = Trails(main=solution_route, branches=[])
    while all_free_points != set():
        free_point = choice(tuple(all_free_points))
        random_walk = _loop_erased_random_walk(N, M, free_point, trails)
        subtrail = trails.get_subtrail_by_point(random_walk[-1])
        subtrail.branches.append(Trails(main=random_walk, branches=[]))

        all_free_points.difference_update(set(random_walk))

    return trails
