"""
Tests of the transforms
"""
import pytest

from limnos.types import Route
from limnos.transforms import (bender,
                               flipper,
                               flattener,
                               Chirality)

two_point_routes = [[(1, 1), (3, 1)],
                    [(1, 1), (1, 3)],
                    [(1, 1), (-1, 1)],
                    [(1, 1), (1, -1)],
                    [(11, 5), (11, 3)]]

three_point_routes = [[(1, 1), (1, 3), (3, 3)],
                      [(1, 1), (1, 3), (-1, 3)],
                      [(1, 1), (3, 1), (3, 3)],
                      [(1, 1), (3, 1), (3, -1)],
                      [(1, 1), (1, -1), (3, -1)],
                      [(1, 1), (1, -1), (-1, -1)],
                      [(1, 1), (-1, 1), (-1, 3)],
                      [(1, 1), (-1, 1), (-1, -1)],
                      [(7, 9), (7, 11), (9, 11)]
                      ]

@pytest.mark.parametrize("route", three_point_routes)
def test_flipper_twice_is_identity(route):
    assert route == flipper(flipper(route, 0), 0)


@pytest.mark.parametrize("chirality", (Chirality.RIGHT, Chirality.LEFT))
@pytest.mark.parametrize("route", two_point_routes)
def test_bend_and_flatten_is_identity(route, chirality):
    bend_route = bender(route, 0, chirality)
    assert flattener(bend_route, 0) == route
