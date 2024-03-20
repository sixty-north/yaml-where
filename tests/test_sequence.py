import pytest
from yaml_where.yaml_where import YAMLWhereSequence
from helpers import clean_yaml, rng
from yaml_where import YAMLWhere
from yaml_where.exceptions import MissingKeyError, UndefinedAccessError


def test_get_top_level():
    yaml = """
    [1,
     a, foo,
     
         indented]
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    assert source_map.get(0) == rng(0, 1, 0, 2)
    assert source_map.get(1) == rng(1, 1, 1, 2)
    assert source_map.get(2) == rng(1, 4, 1, 7)
    assert source_map.get(3) == rng(3, 5, 3, 13)


def test_get_nested():
    yaml = """
    - [1, 2, 34]
    - [3, [4, 5, 6]]
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    assert source_map.get(0) == rng(0, 2, 0, 12)
    assert source_map.get(0, 0) == rng(0, 3, 0, 4)
    assert source_map.get(0, 1) == rng(0, 6, 0, 7)
    assert source_map.get(0, 2) == rng(0, 9, 0, 11)
    assert source_map.get(1, 0) == rng(1, 3, 1, 4)
    assert source_map.get(1, 1) == rng(1, 6, 1, 15)
    assert source_map.get(1, 1, 0) == rng(1, 7, 1, 8)
    assert source_map.get(1, 1, 1) == rng(1, 10, 1, 11)
    assert source_map.get(1, 1, 2) == rng(1, 13, 1, 14)


def test_get_value_top_level():
    yaml = """
    [1,
     a, foo,
     
         indented]
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    assert source_map.get_value(0) == rng(0, 1, 0, 2)
    assert source_map.get_value(1) == rng(1, 1, 1, 2)
    assert source_map.get_value(2) == rng(1, 4, 1, 7)
    assert source_map.get_value(3) == rng(3, 5, 3, 13)


def test_get_value_nested():
    yaml = """
    - [1, 2, 34]
    - [3, [4, 5, 6]]
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    assert source_map.get_value(0) == rng(0, 2, 0, 12)
    assert source_map.get_value(0, 0) == rng(0, 3, 0, 4)
    assert source_map.get_value(0, 1) == rng(0, 6, 0, 7)
    assert source_map.get_value(0, 2) == rng(0, 9, 0, 11)
    assert source_map.get_value(1, 0) == rng(1, 3, 1, 4)
    assert source_map.get_value(1, 1) == rng(1, 6, 1, 15)
    assert source_map.get_value(1, 1, 0) == rng(1, 7, 1, 8)
    assert source_map.get_value(1, 1, 1) == rng(1, 10, 1, 11)
    assert source_map.get_value(1, 1, 2) == rng(1, 13, 1, 14)


def test_get_key_top_level():
    yaml = "[1, 2, 3]"
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    with pytest.raises(UndefinedAccessError):
        source_map.get_key(0)


def test_get_missing_index_top_level():
    yaml = "[1, 2, 3]"
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    with pytest.raises(MissingKeyError):
        source_map.get(4)


def test_get_value_missing_index_top_level():
    yaml = "[1, 2, 3]"
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    with pytest.raises(MissingKeyError):
        source_map.get_value(4)


def test_get_missing_index_nested():
    yaml = "[1, 2, [3, 4, 5]]"
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    with pytest.raises(MissingKeyError):
        source_map.get(2, 3)


def test_get_value_missing_index_nested():
    yaml = "[1, 2, [3, 4, 5]]"
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    with pytest.raises(MissingKeyError):
        source_map.get_value(2, 3)


def test_get_non_integer_key():
    yaml = """
    [1, 2, 3]
    """
    yw = YAMLWhere.from_string(clean_yaml(yaml))
    with pytest.raises(UndefinedAccessError):
        yw.get("a")


def test_get_value_non_integer_key():
    yaml = "[1, 2, 3]"
    with pytest.raises(UndefinedAccessError):
        YAMLWhere.from_string(yaml).get_value("a")


def test_constructor_checks_node_type():
    with pytest.raises(ValueError):
        YAMLWhereSequence(None)