"""
Module that holds the fundamental types and basic functions
"""

Point = tuple[int, int]
Route = list[Point]


def add_points(p1: Point, p2: Point) -> Point:
    """
    Add two Points
    """
    return (p1[0] + p2[0], p1[1] + p2[1])
