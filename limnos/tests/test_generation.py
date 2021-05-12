"""
Test the generation functions
"""
import pytest

from limnos.generation import _wall_intersects_route, random_base_solution


ROUTE = [(1, 1), (1, 3), (3, 3), (5, 3), (5, 5)]
walls = [((2, 2), (4, 2)),
         ((2, 2), (2, 4)),
         ((4, 4), (6, 4))]
intersects = [False, True, True]


@pytest.mark.parametrize("wall, intersects", list(zip(walls, intersects)))
def test_intersection_check(wall, intersects):
    assert _wall_intersects_route(ROUTE, wall) == intersects

def test_random_base_solution:
    # Test should check the following:
    # A) That upper right corner is always the last step (and thus also that
    # it is actually there)
    # B) That there are no points outside of the maze
    # C) It might be a good idea that this test constists of creating several
    # actual mazes and then run the tests on these.
    pass