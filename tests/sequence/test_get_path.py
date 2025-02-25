import pytest
from yaml_where.exceptions import NoSuchPathError
from yaml_where.path import Index
from yaml_where.range import Range
from yaml_where.yaml_where import YAMLWhere
from yaml_where.testing.helpers import clean_yaml

class TestGetTopLevel:
    yaml = """
        [1,
        a, foo,
        
            indented]
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))

    def test_1(self):
        range_0 = self.source_map.get_range(Index(0))
        assert self.source_map.get_path(range_0.start) == (Index(0),)

    def test_2(self):
        range_1 = self.source_map.get_range(Index(1))
        assert  self.source_map.get_path(range_1.start)== (Index(1),)

    def test_3(self):
        range_2 = self.source_map.get_range(Index(2))
        assert self.source_map.get_path(range_2.start) == (Index(2),)

    def test_4(self):
        range_3 = self.source_map.get_range(Index(3))
        assert self.source_map.get_path(range_3.start) == (Index(3),)


def test_nested():
    yaml = """
    [1,
     [2, 3],
     4]
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))

    rng = source_map.get_range(Index(1), Index(1))
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