import pytest
from yaml_where.exceptions import UndefinedAccessError
from yaml_where.range import Range
from yaml_where.yaml_where import YAMLWhere, YAMLWhereScalar


def test_get_top_level_scalar():
    yaml = "hello"
    source_map = YAMLWhere.from_string(yaml)
    assert source_map.get_range() == Range.from_parts(0, 0, 0, 5)


def test_no_argument_non_scalar():
    yaml = """
    - a: 1
    - b: 2
    """
    source_map = YAMLWhere.from_string(yaml)
    with pytest.raises(UndefinedAccessError):
        source_map.get_range()


def test_get_with_key():
    yaml = "hello"
    with pytest.raises(UndefinedAccessError):
        YAMLWhere.from_string(yaml).get_range("a")


def test_get_key():
    yaml = "hello"
    with pytest.raises(UndefinedAccessError):
        YAMLWhere.from_string(yaml).get_key_range("a")


def test_constructor_checks_node_type():
    with pytest.raises(ValueError):
        YAMLWhereScalar(None)