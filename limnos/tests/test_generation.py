"""
Test the generation functions
"""
import pytest

from limnos.generation import _wall_intersects_route
from limnos.generation import trails_generator


ROUTE = [(1, 1), (1, 3), (3, 3), (5, 3), (5, 5)]
walls = [((2, 2), (4, 2)),
         ((2, 2), (2, 4)),
         ((4, 4), (6, 4))]
intersects = [False, True, True]


@pytest.mark.parametrize("wall, intersects", list(zip(walls, intersects)))
def test_intersection_check(wall, intersects):
    assert _wall_intersects_route(ROUTE, wall) == intersects


def test_all_route_points_contain_ints():
    """
    Check that all points on generated routes contain standard ints
    """
    N = 10
    M = 10

    trails = trails_generator(N, M)
    routes = trails.all_routes()

    for route in routes:
        for point in route:
            assert isinstance(point[0], int)
            assert isinstance(point[1], int)
