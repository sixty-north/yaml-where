from yaml_where.range import Position


def test_construct():
    line = 49 
    column = 1337 
    p = Position(line, column)

    assert p.line == line
    assert p.column == column