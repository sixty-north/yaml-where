import pytest
from yaml_where.exceptions import MissingKeyError, UndefinedAccessError
from helpers import rng
from yaml_where.yaml_where import YAMLWhere, YAMLWhereScalar


def test_get_top_level_scalar():
    yaml = "hello"
    source_map = YAMLWhere.from_string(yaml)
    assert source_map.get() == rng(0, 0, 0, 5)


def test_no_argument_non_scalar():
    yaml = """
    - a: 1
    - b: 2
    """
    source_map = YAMLWhere.from_string(yaml)
    with pytest.raises(UndefinedAccessError):
        source_map.get()


def test_get_with_key():
    yaml = "hello"
    with pytest.raises(UndefinedAccessError):
        YAMLWhere.from_string(yaml).get("a")


def test_get_key():
    yaml = "hello"
    with pytest.raises(UndefinedAccessError):
        YAMLWhere.from_string(yaml).get_key("a")


def test_constructor_checks_node_type():
    with pytest.raises(ValueError):
        YAMLWhereScalar(None)