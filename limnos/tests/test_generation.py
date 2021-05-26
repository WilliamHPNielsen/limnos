"""
Test the generation functions
"""
import pytest
from hypothesis import given
import hypothesis.strategies as hst

from limnos.generation import _wall_intersects_route, random_base_solution

ROUTE = [(1, 1), (1, 3), (3, 3), (5, 3), (5, 5)]
walls = [((2, 2), (4, 2)),
         ((2, 2), (2, 4)),
         ((4, 4), (6, 4))]
intersects = [False, True, True]

@pytest.mark.parametrize("wall, intersects", list(zip(walls, intersects)))
def test_intersection_check(wall, intersects):
    assert _wall_intersects_route(ROUTE, wall) == intersects


@given(N=hst.integers(2, 40), M=hst.integers(2, 40))
def test_random_base_solution(N, M):
    this_test = random_base_solution(N, M)
    assert len(this_test) == N + M - 1
    assert this_test[-1] == (N * 2 - 1, M * 2 - 1)