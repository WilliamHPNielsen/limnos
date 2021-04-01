"""
Tests of the transforms
"""
import pytest

from limnos.types import Route
from limnos.transforms import (bender,
                               flipper,
                               flattener,
                               Chirality)

two_point_routes = [[(0, 0), (1, 0)],
                    [(0, 0), (0, 1)],
                    [(0, 0), (-1, 0)],
                    [(0, 0), (0, -1)],
                    [(10, 2), (10, 1)]]

three_point_routes = [[(0, 0), (0, 1), (1, 1)],
                      [(0, 0), (0, 1), (-1, 1)],
                      [(0, 0), (1, 0), (1, 1)],
                      [(0, 0), (1, 0), (1, -1)],
                      [(0, 0), (0, -1), (1, -1)],
                      [(0, 0), (0, -1), (-1, -1)],
                      [(0, 0), (-1, 0), (-1, 1)],
                      [(0, 0), (-1, 0), (-1, -1)],
                      [(3, 7), (4, 7), (4, 8)]
                      ]

@pytest.mark.parametrize("route", three_point_routes)
def test_flipper_twice_is_identity(route):
    assert route == flipper(flipper(route, 0), 0)


@pytest.mark.parametrize("chirality", (Chirality.RIGHT, Chirality.LEFT))
@pytest.mark.parametrize("route", two_point_routes)
def test_bend_and_flatten_is_identity(route, chirality):
    bend_route = bender(route, 0, chirality)
    assert flattener(bend_route, 0) == route
