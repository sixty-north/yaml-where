import pytest
from yaml_where.exceptions import NoSuchPathError, UndefinedAccessError
from yaml_where.range import Position
from yaml_where.yaml_where import YAMLWhere


def test_get():
    yaml = ""
    source_map = YAMLWhere.from_string(yaml)
    with pytest.raises(UndefinedAccessError):
        source_map.get_range()


def test_get_key():
    yaml = ""
    source_map = YAMLWhere.from_string(yaml)
    with pytest.raises(UndefinedAccessError):
        source_map.get_key_range(0)


def test_get_value():
    yaml = ""
    source_map = YAMLWhere.from_string(yaml)
    with pytest.raises(UndefinedAccessError):
        source_map.get_value_range(0)


def test_get_path():
    yaml = ""
    source_map = YAMLWhere.from_string(yaml)
    with pytest.raises(NoSuchPathError):
        source_map.get_path(Position(0, 0))

