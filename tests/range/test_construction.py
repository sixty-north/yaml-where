import pytest
from yaml_where.range import Range


def test_range_beginning():
    r = Range.beginning()
    assert r.start.line == 0
    assert r.start.column == 0
    assert r.end.line == 0
    assert r.end.column == 1


def test_range_beginning_with_arg():
    r = Range.beginning(5)
    assert r.start.line == 0
    assert r.start.column == 0
    assert r.end.line == 0
    assert r.end.column == 5


def test_positions_out_of_order():
    with pytest.raises(ValueError):
        Range.from_parts(1, 1, 0, 0)