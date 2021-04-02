"""
Module to generate mazes
"""
from random import randint

from .types import (Maze,
                    Route,
                    Wall,
                    Walls,
                    add_points,
                    subtract_points)
from .transforms import Direction


def _wall_intersects_route(route: Route, wall: Wall) -> bool:
    """
    Check whether a wall intersects a route. If it does intersect, return
    True.
    """
    wall_delta_coords = subtract_points(*wall)
    route_delta_coords = {(-2, 0): ((1, 1), (1, -1)),
                          (0, -2): ((1, 1), (-1, 1)),
                          (2, 0): ((-1, 1), (-1, -1)),
                          (0, 2): ((1, -1), (-1, -1))}[wall_delta_coords]

    route_p0 = add_points(wall[0], route_delta_coords[0])
    route_p1 = add_points(wall[0], route_delta_coords[1])

    points_in_route = (route_p0 in route) and (route_p1 in route)
    if points_in_route:
        p0_ind = route.index(route_p0)

        # special case: the end of the route
        if p0_ind == len(route) - 1:
            points_neighbours = route[p0_ind - 1] == route_p1
        else:
            points_neighbours = (route[p0_ind + 1] == route_p1 or
                                 route[p0_ind - 1] == route_p1)
    else:
        points_neighbours = False

    return points_in_route and points_neighbours


def _wall_forms_loop(new_wall: Wall, old_walls: Walls) -> bool:
    """
    Check whether adding the new_wall to the old_walls would form
    a closed wall-loop
    """

    p1 = new_wall[0]
    p2 = new_wall[1]

    found_p1 = False
    found_p2 = False

    # TODO: This condition is too strict, sadly, as it prevents
    # ANY gap from being filled, not just loop-forming ones
    for wall in old_walls:
        if not(found_p1):
            if p1 in wall:
                found_p1 = True
        if not(found_p2):
            if p2 in wall:
                found_p2 = True
        if found_p1 and found_p2:
            break

    return found_p1 and found_p2


def add_outer_walls_to_maze(maze: Maze) -> Maze:
    """
    Add the outer walls to a maze
    """

    route: Route = maze[0]
    walls: Walls = maze[1]

    x0 = route[0][0] - 1
    y0 = route[0][1] - 1
    x1 = route[-1][0] + 1
    y1 = route[-1][1] + 1

    bottom: Walls = [((2 * n, 0), (2 * n + 2, 0)) for n in range((x1 - x0)//2)]
    left: Walls = [((0, 2 * n), (0, 2 * n + 2)) for n in range((y1 - y0)//2)]
    right: Walls = [((x1, 2*n), (x1, 2 * n + 2)) for n in range((y1 - y0)//2)]
    top: Walls = [((2 * n, y1), (2 * n + 2, y1)) for n in range((x1 - x0)//2)]

    # remove wall to indicate start and finish
    bottom.pop(0)
    left.pop(0)
    right.pop(-1)
    top.pop(-1)

    return (route, walls + bottom + left + right + top)


def add_random_wall_to_maze(maze: Maze) -> Maze:
    """
    Add a random (inner) wall to a maze
    """

    route: Route = maze[0]
    walls: Walls = maze[1]

    x0 = route[0][0] + 1
    y0 = route[0][1] + 1
    x1 = route[-1][0] - 1
    y1 = route[-1][1] - 1

    found_good_wall = False

    while not(found_good_wall):

        x = 2 * randint(x0 / 2, x1 / 2)
        y = 2 * randint(y0 / 2, y1 / 2)

        step = {1: (0, 2),
                2: (2, 0),
                3: (0, -2),
                4: (-2, 0)}[randint(1, 4)]

        wall: Wall = ((x, y), add_points((x, y), step))

        reasons_to_retry = [wall in walls,
                            _wall_forms_loop(wall, walls),
                            _wall_intersects_route(route, wall)]

        if any(reasons_to_retry):
            pass
        else:
            found_good_wall = True

    new_walls = walls.copy()
    new_walls.append(wall)

    return (route, new_walls)
