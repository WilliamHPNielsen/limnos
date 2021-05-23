"""
Module that holds the fundamental types and basic functions

Note that Routes contain Points of odd coordinates only, whereas
Walls contain Points of even coordinates only
"""
from typing import Union
import json


Point = tuple[int, int]
Route = list[Point]
Routes = list[Route]
Wall = tuple[Point, Point]
Walls = list[Wall]
Maze = tuple[Route, Walls]


TRAILS_SERIAL_VERSION = 1


class Trails():

    def __init__(self, main: Route, branches: list['Trails']):

        self.main: Route = main
        self.branches: list['Trails'] = branches

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

    def serialize(self) -> dict:
        """
        Return a nested dict of dicts of routes containing
        this Trails object
        """
        output = dict()

        def _serializer(trails: Trails, output: dict) -> dict:
            output['main'] = trails.main
            output['branches'] = [_serializer(branch, dict())
                                  for branch in trails.branches]

            return output

        output['version'] = TRAILS_SERIAL_VERSION
        output = _serializer(self, output)

        return output

    def serialize_to_string(self) -> str:
        """
        Return a string representing this Trails object
        """
        return json.dumps(self.serialize())

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
