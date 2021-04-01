"""
Validation of Routes. Contains functions named after rules.
Every function returns a boolean telling whether the rule
is applied to; True means pass/valid, False means fail/invalid
"""
import numpy as np

from .types import Route, Point


def dist_l1(p1: Point, p2: Point) -> int:
    """
    L1 distance between two points
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def all_points_unique(route: Route) -> bool:
    """
    Checks whether all points are unique
    """
    return len(np.unique(route, axis=0)) == len(route)


def all_points_consecutive(route: Route) -> bool:
    """
    Checks whether all points are consecutive, meaning that all points
    neighbour each other
    """

    zipper = zip(route[:-1], route[1:])

    dists = [dist_l1(*points) for points in zipper]

    return bool(np.all(np.array(dists) == 2))


def all_points_inside(route: Route) -> bool:
    """
    Checks whether all points are in the allowed region from
    (1, 1) to the end corner
    """
    start_p = route[0]
    end_p = route[-1]
    dists = [dist_l1(p, start_p) + dist_l1(p, end_p) for p in route]
    threshold = end_p[0] + end_p[1]

    return bool(np.all([dist <= threshold for dist in dists]))


def subroute_flippable(subroute: Route) -> bool:
    """
    Check whether subroute can be flipped. The subroute must
    be three points long and is assumed to be consecutive.
    """
    if len(subroute) != 3:
        raise ValueError('Subroute must be of length 3')

    p1 = subroute[0]
    p2 = subroute[2]

    return abs(p1[0] - p2[0]) == abs(p1[1] - p2[1]) == 2


def subroute_flattenable(subroute: Route) -> bool:
    """
    Check whether subroute can be flattened. The subroute must
    be four points long and is assumed to be consecutive
    """
    if len(subroute) != 4:
        raise ValueError('Subroute must be of length 4')

    p1 = subroute[0]
    p2 = subroute[3]

    return dist_l1(p1, p2) == 2
