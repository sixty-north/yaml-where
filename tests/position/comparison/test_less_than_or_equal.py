from yaml_where.range import Position


def test_different_values():
    p1 = Position(0, 0)
    p2 = Position(1, 1)
    assert p1 <= p2
    assert not p2 <= p1


def test_different_values_same_line():
    p1 = Position(0, 0)
    p2 = Position(0, 1)
    assert p1 <= p2
    assert not p2 <= p1


def test_same_values():
    p1 = Position(1, 2)
    p2 = Position(1, 2)
    assert p1 <= p2
    assert p2 <= p1