from yaml_where.range import Position


def test_different_value():
    p1 = Position(0, 0)
    p2 = Position(1, 1)
    assert p1 != p2
    assert p2 != p1


def test_same_values():
    p1 = Position(0, 0)
    p2 = Position(0, 0)
    assert p1 == p2
    assert p2 == p1