"""
Test the generation functions
"""
import pytest

from limnos.generation import _wall_intersects_route


ROUTE = [(1, 1), (1, 3), (3, 3), (5, 3), (5, 5)]
walls = [((2, 2), (4, 2)),
         ((2, 2), (2, 4)),
         ((4, 4), (6, 4))]
intersects = [False, True, True]


@pytest.mark.parametrize("wall, intersects", list(zip(walls, intersects)))
def test_intersection_check(wall, intersects):
    assert _wall_intersects_route(ROUTE, wall) == intersects
