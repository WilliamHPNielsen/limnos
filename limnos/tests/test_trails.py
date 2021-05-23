"""
Module for testing methods of the Trails object
"""

from limnos.types import Trails
from limnos.generation import trails_generator


def test_serialization_and_deserialization():
    N = 10
    M = 10

    original_trails = trails_generator(N, M)

    recreated_trails = Trails.deserialize(original_trails.serialize())

    # Poor man's equality check, because we haven't implemented
    # __eq__ yet for Trails
    assert str(original_trails) == str(recreated_trails)


def test_serialization_and_deserialization_via_strings():
    N = 10
    M = 10

    original_trails = trails_generator(N, M)

    recreated_trails = Trails.deserialize_from_string(
        original_trails.serialize_to_string())

    # Poor man's equality check, because we haven't implemented
    # __eq__ yet for Trails
    assert str(original_trails) == str(recreated_trails)
