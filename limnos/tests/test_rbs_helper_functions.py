'''
Tests for helper functions for random_base_solution().
'''

from limnos.generation import _topmost, _rightmost, _go_right, _go_up, _random_step

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

def test_go_right():
    assert _go_right((7, 3)) == (9, 3)
    assert _go_right((15, 15)) == (17, 15)

def test_go_up():
    assert _go_up((7, 3)) == (7, 5)
    assert _go_up((15, 15)) == (15, 17)

def test_random_step():
    # Test that the step is either up or right compared to last_point
    test_step = _random_step((7,3))
    assert test_step == (9, 3) or test_step == (7, 5)
    test_step = _random_step((15, 15))
    assert test_step == (17, 15) or test_step == (15, 17)

