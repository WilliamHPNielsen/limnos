"""
Module that holds the fundamental types and basic functions

Note that Routes contain Points of odd coordinates only, whereas
Walls contain Points of even coordinates only
"""
from typing import Union
from enum import Enum, auto

import numpy as np

Point = tuple[int, int]
Route = list[Point]
Routes = list[Route]
Wall = tuple[Point, Point]
Walls = list[Wall]
Maze = tuple[Route, Walls]


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()
    NORTHEAST = auto()
    NORTHWEST = auto()
    SOUTHEAST = auto()
    SOUTHWEST = auto()


NORTH = Direction.NORTH
SOUTH = Direction.SOUTH
EAST = Direction.EAST
WEST = Direction.WEST


def direction_from_points(first: Point, second: Point) -> Direction:
    """
    Helper to get direction from points
    """
    dx = second[0] - first[0]
    dy = second[1] - first[1]

    mapper = {(0, 2): Direction.NORTH,
              (0, -2): Direction.SOUTH,
              (2, 0): Direction.EAST,
              (-2, 0): Direction.WEST}

    if (dx, dy) not in mapper.keys():
        raise ValueError("Invalid non-neighbour points")

    return mapper[(dx, dy)]


class Trails():

    def __init__(self, main: Route, branches: list['Trails']):

        self.main: Route = main
        self._branches: list['Trails'] = branches
        self._impose_canonical_branch_order_2()

    @property
    def branches(self) -> list['Trails']:
        return self._branches

    def add_branch(self, branch: 'Trails'):
        self._branches.append(branch)
        self._impose_canonical_branch_order()

    def _impose_canonical_branch_order(self):
        """
        The canonical branch order: branches are ordered by their appearance
        as the main route is traversed from start to end
        """
        if len(self.branches) == 0:
            return
        inds = [self.main.index(branch.main[0]) for branch in self.branches]
        self._branches = [self.branches[i] for i in np.argsort(inds)]

    def point_in_trails(self, point: Point) -> bool:
        """
        Determine if a point already exists in the trails
        """
        if point in self.main:
            return True
        for branch in self.branches:
            if branch.point_in_trails(point):
                return True
        return False

    def _all_routes(self, routes: Routes) -> Routes:
        routes.append(self.main)
        for branch in self.branches:
            branch._all_routes(routes)
        return routes

    def all_routes(self) -> Routes:
        return self._all_routes([])

    def _get_subtrail_by_point(self,
                               point: Point,
                               lst: list['Trails']) -> list['Trails']:
        if point in self.main:
            lst.append(self)
        else:
            for branch in self.branches:
                branch._get_subtrail_by_point(point, lst)

        return lst

    def get_subtrail_by_point(self, point: Point) -> 'Trails':
        """
        Get the subtrail that contains the point in its main trail
        """
        if not(self.point_in_trails(point)):
            raise ValueError("Point not in trails")
        else:
            trails = self._get_subtrail_by_point(point, [])[0]

        return trails

    def __getitem__(self, key: list[int]) -> 'Trails':
        if len(key) == 1:
            return self.branches[key[0]]
        else:
            return self.branches[key[0]][key[1:]]

    def __repr__(self) -> str:
        return f"Trail({self.main}, {self.branches})"


def add_points(p1: Point, p2: Point) -> Point:
    """
    Add two Points
    """
    return (p1[0] + p2[0], p1[1] + p2[1])


def subtract_points(p1: Point, p2: Point) -> Point:
    """
    Subtract two points
    """
    return (p1[0] - p2[0], p1[1] - p2[1])
