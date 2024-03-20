import pytest
from helpers import clean_yaml
from yaml_where import YAMLWhere
from yaml_where.range import Position, Range


def test_get_top_level():
    source_map = YAMLWhere.from_string("a: 1\nb: 42")
    assert source_map.get("a") == Range(Position(0, 0), Position(0, 4))
    assert source_map.get("b") == Range(Position(1, 0), Position(1, 5))


def test_get_nested():
    yaml = """
    a:
        b: 42
        c:
            d: hola
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    assert source_map.get("a", "b") == Range(Position(1, 4), Position(1, 9))
    assert source_map.get("a", "c") == Range(Position(2, 4), Position(3, 15))
    assert source_map.get("a", "c", "d") == Range(Position(3, 8), Position(3, 15))


def test_get_key_top_level():
    source_map = YAMLWhere.from_string("a: 1\nbb: 42")
    assert source_map.get_key("a") == Range(Position(0, 0), Position(0, 1))
    assert source_map.get_key("bb") == Range(Position(1, 0), Position(1, 2))


def test_get_key_nested():
    yaml = """
    a:
        b: 42
        c:
            doo: hola
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    assert source_map.get_key("a", "b") == Range(Position(1, 4), Position(1, 5))
    assert source_map.get_key("a", "c") == Range(Position(2, 4), Position(2, 5))
    assert source_map.get_key("a", "c", "doo") == Range(Position(3, 8), Position(3, 11))


def test_get_value_top_level():
    source_map = YAMLWhere.from_string("a: 1\nbb: 42")
    assert source_map.get_value("a") == Range(Position(0, 3), Position(0, 4))
    assert source_map.get_value("bb") == Range(Position(1, 4), Position(1, 6))


def test_get_value_nested():
    yaml = """
    a:
        b: 42
        c:
            doo: hola
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    assert source_map.get_value("a", "b") == Range(Position(1, 7), Position(1, 9))
    assert source_map.get_value("a", "c") == Range(Position(3, 8), Position(3, 17))
    assert source_map.get_value("a", "c", "doo") == Range(Position(3, 13), Position(3, 17))

def test_get_top_level_missing_key():
    source_map = YAMLWhere.from_string("a: 1\nb: 42")
    with pytest.raises(KeyError):
        source_map.get("c")


def test_get_nested_missing_key():
    yaml = """
    a:
        b: 42
        c:
            d: hola
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    with pytest.raises(KeyError):
        source_map.get("a", "e")


def test_get_key_top_level_missing_key():
    source_map = YAMLWhere.from_string("a: 1\nbb: 42")
    with pytest.raises(KeyError):
        source_map.get_key("c")


def test_get_key_nested_missing_key():
    yaml = """
    a:
        b: 42
        c:
            doo: hola
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    with pytest.raises(KeyError):
        source_map.get_key("a", "c", "llama")


def test_get_value_top_level_missing_key():
    source_map = YAMLWhere.from_string("a: 1\nbb: 42")
    with pytest.raises(KeyError):
        source_map.get_value("c")


def test_get_value_nested_missing_key():
    yaml = """
    a:
        b: 42
        c:
            doo: hola
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    with pytest.raises(KeyError):
        source_map.get_value("a", "b", "q")


