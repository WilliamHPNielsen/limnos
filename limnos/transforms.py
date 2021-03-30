"""
Route transformations
"""
from enum import Enum, auto

from .types import Point, Route, add_points


class Chirality(Enum):
    LEFT = auto()
    RIGHT = auto()


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


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


def flipper():
    pass


def flattener():
    pass
