from yaml_where.range import Position, Range


def test_point_in_range():
    range = Range(Position(0, 0), Position(1, 1))
    point = Position(0, 4)
    assert point in range


def test_point_at_start():
    range = Range(Position(0, 0), Position(1, 1))
    point = Position(0, 0)
    assert point in range

def test_point_at_end():
    range = Range(Position(0, 0), Position(1, 1))
    point = Position(1, 1)
    assert point not in range

def test_point_one_before_end():
    range = Range(Position(0, 0), Position(1, 1))
    point = Position(1, 0)
    assert point in range

def test_point_after_range():
    range = Range(Position(0, 0), Position(1, 1))
    point = Position(2, 2)
    assert point not in range


def test_point_before_range():
    range = Range(Position(1, 1), Position(2, 2))
    point = Position(0, 0)
    assert point not in range


def test_contains_point_negative_coordinates():
    range = Range(Position(-1, -1), Position(1, 1))
    point = Position(0, 0)
    assert point in range


def test_contains_point_outside_negative_coordinates():
    range = Range(Position(-1, -1), Position(1, 1))
    point = Position(-2, -2)
    assert point not in range
