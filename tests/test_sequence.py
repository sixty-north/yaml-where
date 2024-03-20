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


def test_get_nested_mapping_entry():
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


# def test_get_key_top_level():
#     source_map = YAMLWhere.from_string("a: 1\nbb: 42")
#     assert source_map.get_key("a") == Range(Position(0, 0), Position(0, 1))
#     assert source_map.get_key("bb") == Range(Position(1, 0), Position(1, 2))


# def test_get_key_nested():
#     yaml = """
#     a:
#         b: 42
#         c:
#             doo: hola
#     """
#     source_map = YAMLWhere.from_string(clean_yaml(yaml))
#     assert source_map.get_key("a", "b") == Range(Position(1, 4), Position(1, 5))
#     assert source_map.get_key("a", "c") == Range(Position(2, 4), Position(2, 5))
#     assert source_map.get_key("a", "c", "doo") == Range(Position(3, 8), Position(3, 11))


# def test_get_value_top_level():
#     source_map = YAMLWhere.from_string("a: 1\nbb: 42")
#     assert source_map.get_value("a") == Range(Position(0, 3), Position(0, 4))
#     assert source_map.get_value("bb") == Range(Position(1, 4), Position(1, 6))


# def test_get_value_nested():
#     yaml = """
#     a:
#         b: 42
#         c:
#             doo: hola
#     """
#     source_map = YAMLWhere.from_string(clean_yaml(yaml))
#     assert source_map.get_value("a", "b") == Range(Position(1, 7), Position(1, 9))
#     assert source_map.get_value("a", "c") == Range(Position(3, 8), Position(3, 17))
#     assert source_map.get_value("a", "c", "doo") == Range(Position(3, 13), Position(3, 17))


# TODO:
# - get() in sequence
# - get_key() in sequence (raises)
# - get_value() in sequence (same as get())
# - test arbitrary nesting
# - test exceptions
# - numeric indices
# - top-level scalars