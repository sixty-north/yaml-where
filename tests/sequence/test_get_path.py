import pytest
from yaml_where.exceptions import NoSuchPathError
from yaml_where.path import Index
from yaml_where.range import Range
from yaml_where.yaml_where import YAMLWhere
from yaml_where.testing.helpers import clean_yaml

def test_get_top_level():
    yaml = """
    [1,
     a, foo,
     
         indented]
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))

    range_0 = source_map.get_range(0)
    assert source_map.get_path(range_0.start) == (Index(0),)

    range_1 = source_map.get_range(1)
    assert  source_map.get_path(range_1.start)== (Index(1),)

    range_2 = source_map.get_range(2)
    assert source_map.get_path(range_2.start) == (Index(2),)

    range_3 = source_map.get_range(3)
    assert source_map.get_path(range_3.start) == (Index(3),)


def test_nested():
    yaml = """
    [1,
     [2, 3],
     4]
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))

    rng = source_map.get_range(1, 1)
    assert source_map.get_path(rng.start) == (Index(1), Index(1))


def test_not_found():
    yaml = """
    [1,
     [2, 3],
     4]
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    rng = Range.from_parts(10, 0, 10, 4)

    with pytest.raises(NoSuchPathError):
        source_map.get_path(rng.start)