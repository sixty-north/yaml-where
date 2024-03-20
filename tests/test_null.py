import pytest
from yaml_where.exceptions import UndefinedAccessError
from yaml_where.yaml_where import YAMLWhere


def test_get():
    yaml = ""
    source_map = YAMLWhere.from_string(yaml)
    with pytest.raises(UndefinedAccessError):
        source_map.get()


def test_get_key():
    yaml = ""
    source_map = YAMLWhere.from_string(yaml)
    with pytest.raises(UndefinedAccessError):
        source_map.get_key(0)


def test_get_value():
    yaml = ""
    source_map = YAMLWhere.from_string(yaml)
    with pytest.raises(UndefinedAccessError):
        source_map.get_value(0)