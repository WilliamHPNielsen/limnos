'''
Tests for helper functions for random_base_solution().
'''

from limnos.generation import _topmost, _rightmost

def test_topmost():
    assert _topmost((5, 7), 4) == True
    assert _topmost((5, 3), 4) == False
    assert _topmost((7, 1), 4) == False
    assert _topmost((7, 9), 5) == True

def test_rightmost():
    assert _rightmost((15, 3), 8) == True
    assert _rightmost((5, 11), 3) == True
    assert _rightmost((7, 11), 8) == False
    assert _rightmost((9, 47), 24) == False