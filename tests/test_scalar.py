import pytest
from yaml_where.range import Position, Range
from yaml_where.yaml_where import YAMLWhere


def test_get_top_level_scalar():
    yaml = "hello"
    source_map = YAMLWhere.from_string(yaml)
    assert source_map.get() == Range(Position(0, 0), Position(0, 5))


def test_no_argument_non_scalar():
    yaml = """
    - a: 1
    - b: 2
    """
    source_map = YAMLWhere.from_string(yaml)
    with pytest.raises(ValueError):
        source_map.get()