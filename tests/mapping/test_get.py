import pytest
from yaml_where.range import Range
from yaml_where.yaml_where import YAMLWhereMapping
from yaml_where.testing.helpers import clean_yaml
from yaml_where import YAMLWhere
from yaml_where.exceptions import MissingKeyError, UndefinedAccessError


def test_top_level():
    source_map = YAMLWhere.from_string("a: 1\nb: 42")
    assert source_map.get("a") == Range.from_parts(0, 0, 0, 4)
    assert source_map.get("b") == Range.from_parts(1, 0, 1, 5)


def test_nested():
    yaml = """
    a:
        b: 42
        c:
            d: hola
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    assert source_map.get("a", "b") == Range.from_parts(1, 4, 1, 9)
    # assert source_map.get("a", "c") == Range.from_parts(2, 4, 3, 15)
    # assert source_map.get("a", "c", "d") == Range.from_parts(3, 8, 3, 15)


def test_key_top_level():
    source_map = YAMLWhere.from_string("a: 1\nbb: 42")
    assert source_map.get_key("a") == Range.from_parts(0, 0, 0, 1)
    assert source_map.get_key("bb") == Range.from_parts(1, 0, 1, 2)


def test_key_nested():
    yaml = """
    a:
        b: 42
        c:
            doo: hola
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    assert source_map.get_key("a", "b") == Range.from_parts(1, 4, 1, 5)
    # assert source_map.get_key("a", "c") == Range.from_parts(2, 4, 2, 5)
    # assert source_map.get_key("a", "c", "doo") == Range.from_parts(3, 8, 3, 11)


def test_value_top_level():
    source_map = YAMLWhere.from_string("a: 1\nbb: 42")
    assert source_map.get_value("a") == Range.from_parts(0, 3, 0, 4)
    assert source_map.get_value("bb") == Range.from_parts(1, 4, 1, 6)


def test_value_nested():
    yaml = """
    a:
        b: 42
        c:
            doo: hola
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    assert source_map.get_value("a", "b") == Range.from_parts(1, 7, 1, 9)
    assert source_map.get_value("a", "c") == Range.from_parts(3, 8, 3, 17)
    assert source_map.get_value("a", "c", "doo") == Range.from_parts(3, 13, 3, 17)


def test_top_level_missing_key():
    source_map = YAMLWhere.from_string("a: 1\nb: 42")
    with pytest.raises(MissingKeyError):
        source_map.get("c")


def test_nested_missing_key():
    yaml = """
    a:
        b: 42
        c:
            d: hola
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    with pytest.raises(MissingKeyError):
        source_map.get("a", "e")


def test_key_top_level_missing_key():
    source_map = YAMLWhere.from_string("a: 1\nbb: 42")
    with pytest.raises(MissingKeyError):
        source_map.get_key("c")


def test_key_nested_missing_key():
    yaml = """
    a:
        b: 42
        c:
            doo: hola
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    with pytest.raises(MissingKeyError):
        source_map.get_key("a", "c", "llama")


def test_value_top_level_missing_key():
    source_map = YAMLWhere.from_string("a: 1\nbb: 42")
    with pytest.raises(MissingKeyError):
        source_map.get_value("c")


def test_value_nested_missing_key():
    yaml = """
    a:
        b: 42
        c:
            doo: hola
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    with pytest.raises(UndefinedAccessError):
        source_map.get_value("a", "b", "q")


def test_constructor_checks_node_type():
    with pytest.raises(ValueError):
        YAMLWhereMapping(None)


def test_with_no_keys():
    yaml = """
    a:
        b: 42
        c:
            doo: hola
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    with pytest.raises(UndefinedAccessError):
        source_map.get()