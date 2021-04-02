"""
Module that holds the fundamental types and basic functions

Note that Routes contain Points of odd coordinates only, whereas
Walls contain Points of even coordinates only
"""

Point = tuple[int, int]
Route = list[Point]
Wall = tuple[Point, Point]
Walls = list[Wall]
Maze = tuple[Route, Walls]


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
