import pytest
from yaml_where.exceptions import UndefinedAccessError
from helpers import rng
from yaml_where.yaml_where import YAMLWhere


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
