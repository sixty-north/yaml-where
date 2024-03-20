from yaml_where.range import Position, Range
from helpers import clean_yaml
from yaml_where import YAMLWhere


def test_get_top_level():
    yaml = """
    [1,
     a, foo,
     
         indented]
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    assert source_map.get(0) == Range(Position(0, 1), Position(0, 2))
    assert source_map.get(1) == Range(Position(1, 1), Position(1, 2))
    assert source_map.get(2) == Range(Position(1, 4), Position(1, 7))
    assert source_map.get(3) == Range(Position(3, 5), Position(3, 13))


def test_get_nested():
    yaml = """
    - [1, 2, 34]
    - [3, [4, 5, 6]]
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    assert source_map.get(0) == Range(Position(0, 2), Position(0, 12))
    assert source_map.get(0, 0) == Range(Position(0, 3), Position(0, 4))
    assert source_map.get(0, 1) == Range(Position(0, 6), Position(0, 7))
    assert source_map.get(0, 2) == Range(Position(0, 9), Position(0, 11))
    assert source_map.get(1, 0) == Range(Position(1, 3), Position(1, 4))
    assert source_map.get(1, 1) == Range(Position(1, 6), Position(1, 15))
    assert source_map.get(1, 1, 0) == Range(Position(1, 7), Position(1, 8))
    assert source_map.get(1, 1, 1) == Range(Position(1, 10), Position(1, 11))
    assert source_map.get(1, 1, 2) == Range(Position(1, 13), Position(1, 14))


def test_get_value_top_level():
    yaml = """
    [1,
     a, foo,
     
         indented]
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    assert source_map.get_value(0) == Range(Position(0, 1), Position(0, 2))
    assert source_map.get_value(1) == Range(Position(1, 1), Position(1, 2))
    assert source_map.get_value(2) == Range(Position(1, 4), Position(1, 7))
    assert source_map.get_value(3) == Range(Position(3, 5), Position(3, 13))

def test_get_value_nested():
    yaml = """
    - [1, 2, 34]
    - [3, [4, 5, 6]]
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    assert source_map.get_value(0) == Range(Position(0, 2), Position(0, 12))
    assert source_map.get_value(0, 0) == Range(Position(0, 3), Position(0, 4))
    assert source_map.get_value(0, 1) == Range(Position(0, 6), Position(0, 7))
    assert source_map.get_value(0, 2) == Range(Position(0, 9), Position(0, 11))
    assert source_map.get_value(1, 0) == Range(Position(1, 3), Position(1, 4))
    assert source_map.get_value(1, 1) == Range(Position(1, 6), Position(1, 15))
    assert source_map.get_value(1, 1, 0) == Range(Position(1, 7), Position(1, 8))
    assert source_map.get_value(1, 1, 1) == Range(Position(1, 10), Position(1, 11))
    assert source_map.get_value(1, 1, 2) == Range(Position(1, 13), Position(1, 14))



# TODO:
# - get_key() in sequence (raises)
# - test arbitrary nesting
# - test exceptions
# - numeric indices
# - top-level scalars