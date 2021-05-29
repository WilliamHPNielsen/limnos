"""
Module that holds the fundamental types and basic functions

Note that Routes contain Points of odd coordinates only, whereas
Walls contain Points of even coordinates only
"""
from typing import Union
from enum import Enum, auto

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
        self._branches: list['Trails'] = []
        for branch in branches:
            self.add_branch(branch)

    @property
    def branches(self) -> list['Trails']:
        return self._branches

    def add_branch(self, branch: 'Trails'):
        self._branches.append(branch)
        self._impose_canonical_branch_order()

    def _impose_canonical_branch_order(self):

        def _assign_branch_number(branch: 'Trails') -> int:

            main_index = self.main.index(branch.main[0])

            # special cases of the end and start points
            # where no 4-way cross can occur
            if main_index == len(self.main) - 1 or main_index == 0:
                return main_index * 2

            main_dir_pre = direction_from_points(self.main[main_index],
                                                 self.main[main_index - 1])
            main_dir_post = direction_from_points(self.main[main_index + 1],
                                                  self.main[main_index])
            branch_direction = direction_from_points(branch.main[1],
                                                     branch.main[0])
            does_branch_go_left = {
                (NORTH, NORTH, EAST): False,
                (NORTH, NORTH, WEST): True,
                (NORTH, EAST, WEST): True,
                (NORTH, EAST, NORTH): False,
                (NORTH, WEST, EAST): False,
                (NORTH, WEST, NORTH): True,
                (SOUTH, SOUTH, EAST): True,
                (SOUTH, SOUTH, WEST): False,
                (SOUTH, EAST, SOUTH): True,
                (SOUTH, EAST, WEST): False,
                (SOUTH, WEST, SOUTH): False,
                (SOUTH, WEST, EAST): True,
                (EAST, EAST, NORTH): True,
                (EAST, EAST, SOUTH): False,
                (EAST, NORTH, SOUTH): False,
                (EAST, NORTH, EAST): True,
                (EAST, SOUTH, NORTH): True,
                (EAST, SOUTH, EAST): False,
                (WEST, WEST, NORTH): False,
                (WEST, WEST, SOUTH): True,
                (WEST, NORTH, SOUTH): True,
                (WEST, NORTH, WEST): False,
                (WEST, SOUTH, WEST): True,
                (WEST, SOUTH, NORTH): False}
            branch_goes_left = does_branch_go_left[(main_dir_pre,
                                                    main_dir_post,
                                                    branch_direction)]
            branch_number = main_index * 2 - (1 if branch_goes_left else 0)

            return branch_number

        self._branches = sorted(self._branches, key=_assign_branch_number)

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

    def __eq__(self, other):

        def _any_difference(self, other):
            if not isinstance(other, Trails):
                return True
            if self.main != other.main:
                return True
            if len(self.branches) != len(other.branches):
                return True
            for b1, b2 in zip(self.branches, other.branches):
                _any_difference(b1, b2)

        if _any_difference(self, other):
            return False
        else:
            return True


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
