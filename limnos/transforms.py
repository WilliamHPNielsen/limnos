"""
Route transformations
"""
from enum import Enum, auto
from functools import partial
from random import randint

from .types import (Point,
                    Route,
                    add_points,
                    subtract_points)
from .validation import (all_points_consecutive,
                         all_points_inside,
                         all_points_unique,
                         subroute_flippable,
                         subroute_flattenable)


class Chirality(Enum):
    LEFT = auto()
    RIGHT = auto()


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()
    NORTHEAST = auto()
    NORTHWEST = auto()
    SOUTHEAST = auto()
    SOUTHWEST = auto()


def _direction_from_points(first: Point, second: Point) -> Direction:
    """
    Helper to get direction from points
    """
    dx = second[0] - first[0]
    dy = second[1] - first[1]

    mapper = {(0, 1): Direction.NORTH,
              (0, -1): Direction.SOUTH,
              (1, 0): Direction.EAST,
              (-1, 0): Direction.WEST}

    if (dx, dy) not in mapper.keys():
        raise ValueError("Invalid non-neighbour points")

    return mapper[(dx, dy)]


def _new_bender_points(starting_point: Point,
                       direction: Direction,
                       chirality: Chirality) -> tuple[Point, Point]:
    """
    Subroutine for bender transform
    """
    # chirality == right
    delta_ps_right = {Direction.NORTH: [(1, 0), (1, 1)],
                      Direction.SOUTH: [(-1, 0), (-1, -1)],
                      Direction.EAST: [(0, -1), (1, -1)],
                      Direction.WEST: [(0, 1), (-1, 1)]}
    # chirality == left
    delta_ps_left = {Direction.NORTH: [(-1, 0), (-1, 1)],
                     Direction.SOUTH: [(1, 0), (1, -1)],
                     Direction.EAST: [(0, 1), (1, 1)],
                     Direction.WEST: [(0, -1), (-1, -1)]}

    delta_ps = {Chirality.RIGHT: delta_ps_right,
                Chirality.LEFT: delta_ps_left}[chirality][direction]

    new_points = (add_points(starting_point, delta_ps[0]),
                  add_points(starting_point, delta_ps[1]))

    return new_points


def _direction_from_next_neighbor_points(p1: Point,
                                         p2: Point) -> Direction:
    """
    Get the direction between two next-neighbour points
    """
    dp = subtract_points(p2, p1)

    mapper = {(1, 1): Direction.NORTHEAST,
              (-1, 1): Direction.NORTHWEST,
              (1, -1): Direction.SOUTHEAST,
              (-1, -1): Direction.SOUTHWEST}

    return mapper[dp]


def bender(route: Route, start: int, chirality: Chirality) -> Route:
    """
    Make a 2-point transform, a bend, which adds two new points
    to the route. A "-" becomes a "U"

    Args:
      route: the Route to transform
      starting_point: the first point to change
      direction: which way to bend
    """

    if start >= len(route):
        raise ValueError("Invalid first point")

    p1 = route[start]
    p2 = route[start + 1]

    direction = _direction_from_points(p1, p2)

    new_points = _new_bender_points(p1, direction, chirality)

    new_route = route.copy()

    new_route.insert(start + 1, new_points[1])
    new_route.insert(start + 1, new_points[0])

    return new_route


def flipper(route: Route, start: int) -> Route:
    """
    Make a 3-point transform, a flip, which conserves the number
    of points in the route.
    """
    subroute = route[start: start + 3]

    if not(subroute_flippable(subroute)):
        raise ValueError("Subroute not flippable, cannot proceed")

    start_point = subroute[0]
    flip_point = subroute[1]
    end_point = subroute[2]

    same_x = flip_point[0] == start_point[0]

    direction = _direction_from_next_neighbor_points(start_point, end_point)

    flip_map = {(Direction.NORTHEAST, True): (1, -1),
                (Direction.NORTHEAST, False): (-1, 1),
                (Direction.SOUTHWEST, True): (-1, 1),
                (Direction.SOUTHWEST, False): (1, -1),
                (Direction.NORTHWEST, True): (-1, -1),
                (Direction.NORTHWEST, False): (1, 1),
                (Direction.SOUTHEAST, True): (1, 1),
                (Direction.SOUTHEAST, False): (-1, -1)}

    delta_coords = flip_map[(direction, same_x)]

    new_route = route.copy()

    new_route[start + 1] = add_points(route[start + 1], delta_coords)

    return new_route


def flattener(route: Route, start: int):
    """
    Make a 4-point transform, a flattening, which turns a "U" into an "I"
    by removing two points
    """
    subroute = route[start: start + 4]

    if not(subroute_flattenable(subroute)):
        raise ValueError('Subroute not flattenable, cannot proceed')

    new_route = route.copy()

    new_route.pop(start + 1)
    new_route.pop(start + 1)

    return new_route


def randomly_transform_once(route: Route) -> Route:
    """
    Apply one random transformation
    """
    # partially apply chirality to bender and have four
    # basic transforms?
    # partial(bender, chirality=Chirality.RIGHT) etc.
    # probability weights 1/6, 1/6, 1/3, 1/3
    transforms = {1: partial(bender, chirality=Chirality.RIGHT),
                  2: partial(bender, chirality=Chirality.LEFT),
                  3: flipper,
                  4: flipper,
                  5: flattener,
                  6: flattener}

    found_valid_transform = False
    tries = 0

    while not(found_valid_transform) and tries < 50:
        tries += 1
        transform_to_try = transforms[randint(1, 6)]
        point_to_try = randint(0, len(route) - 1)

        try:
            new_route = transform_to_try(route, point_to_try)
        except (ValueError, IndexError):
            continue

        cons = all_points_consecutive(new_route)
        uniq = all_points_unique(new_route)
        ins = all_points_inside(new_route)

        if cons and uniq and ins:
            found_valid_transform = True

    return new_route
