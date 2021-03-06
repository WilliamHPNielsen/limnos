"""
Module to generate mazes
"""
from random import randint, choice
from typing import Optional, cast

import numpy as np

from .types import (Maze,
                    Point,
                    Route,
                    Trails,
                    Wall,
                    Walls,
                    add_points,
                    subtract_points)
from .transforms import Direction, randomly_transform_N_times


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

        x = 2 * randint(x0 // 2, x1 // 2)
        y = 2 * randint(y0 // 2, y1 // 2)

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


def _legal_sprout_point(route: Route, route_branch: Route, point: Point):
    x, y = point
    x_in_range = x >= 1 and x <= route[-1][0]
    y_in_range = y >= 1 and y <= route[-1][1]
    point_in_the_clear = (point not in route) and (point not in route_branch)

    return x_in_range and y_in_range and point_in_the_clear


def sprout_new_random_branch(mother_trails: Trails,
                             sub_trails: Trails,
                             start: int) -> Optional[Trails]:
    """
    Sprout a new random branch onto a sub trail

    Args:
        mother_trails: The main/full trails of the maze
          (containing also the subtrail)
        sub_trails: The trails where the branch should go
        start: the sprout point of the branch on the main of the
          sub_trails

    Returns:
        A new trails with the sprouted branch as main OR None if
          no legal sprouting was possible
    """

    more_steps_possible = True
    head = sub_trails.main[start]

    branch_route: Route = [head]

    north_step = (0, 2)
    west_step = (-2, 0)
    east_step = (2, 0)
    south_step = (0, -2)

    steps = np.array([north_step, east_step, south_step, west_step])

    while more_steps_possible:
        points = [add_points(head, step) for step in steps]
        possible_steps = []
        for point, step in zip(points, steps):
            cond_1 = not(mother_trails.point_in_trails(point))
            cond_2 = _legal_sprout_point(mother_trails.main, branch_route, point)
            if cond_1 and cond_2:
                possible_steps.append(step)

        if len(possible_steps) > 0:
            step = possible_steps[randint(0, len(possible_steps) - 1)]
            # now cast numpy ints to standard ints since some modules
            # (notably json) care about the int type
            step = (int(step[0]), int(step[1]))
            head = add_points(head, step)
            branch_route.append(head)
        else:
            more_steps_possible = False

    if len(branch_route) == 1:
        branch_route = []
        new_trails = None
    else:
        new_trails = Trails(main=branch_route, branches=[])

    return new_trails


def sprout_new_random_route(route: Route, start: int) -> Route:
    """
    Sprout a new route that fits onto an existing route, i.e. only touches it
    in one place, namely the starting point
    """

    more_steps_possible = True
    head = route[start]

    route_branch = [head]

    north_step = (0, 2)
    west_step = (-2, 0)
    east_step = (2, 0)
    south_step = (0, -2)

    steps = np.array([north_step, east_step, south_step, west_step])

    while more_steps_possible:

        possible_steps = steps[[_legal_sprout_point(route, route_branch, add_points(head, step))
                                for step in steps]]
        if len(possible_steps) > 0:
            step = possible_steps[randint(0, len(possible_steps) - 1)]
            head = add_points(head, step)
            route_branch.append(head)
            print(route_branch)
        else:
            more_steps_possible = False

    if len(route_branch) == 1:
        route_branch = []

    return route_branch


def _close_trail_point(trails: Trails, free_point: Point) -> Point:
    """
    helper function to get a point in trails close to a free point
    no guarentees that it's the nearest point

    NB: a hit is guarenteed since the solution route goes from the
    SW corner to the NE corner
    """
    if trails.point_in_trails(free_point):
        return free_point

    found_point = False
    dist = 0
    while not(found_point):
        dist += 2
        new_points = [add_points(free_point, (dist, 0)),
                      add_points(free_point, (0, dist)),
                      add_points(free_point, (-dist, 0)),
                      add_points(free_point, (0, -dist))]
        for new_point in new_points:
            if trails.point_in_trails(new_point):
                found_point = True
                break

    return new_point


def trails_generator(N: int, M: int) -> Trails:
    """
    Full trail generation, generates N x M system
    """

    all_free_points: set[Point] = set(
        [(2*n + 1, 2*m + 1) for n in range(N) for m in range(M)])

    solution_route: Route = ([(1, 2*m + 1) for m in range(M)] +
                             [(2*(n + 1) + 1, 2*(M - 1) + 1)
                              for n in range(N - 1)])

    # TODO: What's an appropriate number of transformations?
    solution_route = randomly_transform_N_times(solution_route, N * M)

    all_free_points.difference_update(set(solution_route))

    trails = Trails(main=solution_route, branches=[])

    while all_free_points != set():
        free_point = choice(tuple(all_free_points))
        trail_point = _close_trail_point(trails, free_point)
        subtrail = trails.get_subtrail_by_point(trail_point)
        start = subtrail.main.index(trail_point)
        new_trail = sprout_new_random_branch(trails, subtrail, start)
        new_trail = cast(Trails, new_trail)
        subtrail.branches.append(new_trail)
        all_free_points.difference_update(set(new_trail.main))

    return trails


def _all_potential_walls(trails: Trails) -> Walls:
    """
    Helper function to generate all possible walls in the rectangle
    defined by the extremal points of the highest route in the trails
    """
    x0 = trails.main[0][0] - 1
    x1 = trails.main[-1][0] + 1
    y0 = trails.main[0][1] - 1
    y1 = trails.main[-1][1] + 1

    horiz_walls: Walls = [((x, y), (x + 2, y))
                          for x in range(x0, x1, 2)
                          for y in range(y0, y1 + 2, 2)]
    vert_walls: Walls = [((x, y), (x, y + 2))
                         for x in range(x0, x1 + 2, 2)
                         for y in range(y0, y1, 2)]

    return horiz_walls + vert_walls


def walls_from_trails(trails: Trails) -> Walls:
    """
    Generate the walls that complement all the routes in a Trails collection.
    All possible allowed walls are generated.
    """

    walls = _all_potential_walls(trails)
    forbidden_walls = []

    routes = trails.all_routes()

    for wall in walls:
        w1 = wall
        w2 = (wall[1], wall[0])
        for route in routes:
            intersect1 = _wall_intersects_route(route, w1)
            intersect2 = _wall_intersects_route(route, w2)
            if intersect1 or intersect2:
                forbidden_walls.append(wall)

    legal_walls = [wall for wall in walls if wall not in forbidden_walls]

    return legal_walls
