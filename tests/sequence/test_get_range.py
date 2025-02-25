import pytest
from yaml_where.path import Index, Key
from yaml_where.range import Range
from yaml_where.yaml_where import YAMLWhereSequence
from yaml_where.testing.helpers import clean_yaml
from yaml_where import YAMLWhere
from yaml_where.exceptions import MissingKeyError, UndefinedAccessError


class TestGetTopLevel:
    yaml = """
    [1,
     a, foo,
    
         indented]
        
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))

    def test_1(self):
        assert self.source_map.get_range(Index(0)) == Range.from_parts(0, 1, 0, 2)

    def test_2(self):
        assert self.source_map.get_range(Index(1)) == Range.from_parts(1, 1, 1, 2)

    def test_3(self):
        assert self.source_map.get_range(Index(2)) == Range.from_parts(1, 4, 1, 7)

    def test_4(self):
        assert self.source_map.get_range(Index(3)) == Range.from_parts(3, 5, 3, 13)


class TestGetNested:
    yaml = """
    - [1, 2, 34]
    - [3, [4, 5, 6]]
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))

    def test_1(self):
        assert self.source_map.get_range(Index(0)) == Range.from_parts(0, 2, 0, 12)

    def test_2(self):
        assert self.source_map.get_range(Index(0), Index(0)) == Range.from_parts(0, 3, 0, 4)

    def test_3(self):
        assert self.source_map.get_range(Index(0), Index(1)) == Range.from_parts(0, 6, 0, 7)

    def test_4(self):
        assert self.source_map.get_range(Index(0), Index(2)) == Range.from_parts(0, 9, 0, 11)

    def test_5(self):
        assert self.source_map.get_range(Index(1), Index(0)) == Range.from_parts(1, 3, 1, 4)

    def test_6(self):
        assert self.source_map.get_range(Index(1), Index(1)) == Range.from_parts(1, 6, 1, 15)

    def test_7(self):
        assert self.source_map.get_range(Index(1), Index(1), Index(0)) == Range.from_parts(1, 7, 1, 8)

    def test_8(self):
        assert self.source_map.get_range(Index(1), Index(1), Index(1)) == Range.from_parts(1, 10, 1, 11)

    def test_9(self):
        assert self.source_map.get_range(Index(1), Index(1), Index(2)) == Range.from_parts(1, 13, 1, 14)


def test_get_missing_index_top_level():
    yaml = "[1, 2, 3]"
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    with pytest.raises(MissingKeyError):
        source_map.get_range(Index(4))


def test_get_missing_index_nested():
    yaml = "[1, 2, [3, 4, 5]]"
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    with pytest.raises(MissingKeyError):
        source_map.get_range(Index(2), Index(3))


def test_get_non_integer_key():
    yaml = """
    [1, 2, 3]
    """
    yw = YAMLWhere.from_string(clean_yaml(yaml))
    with pytest.raises(UndefinedAccessError):
        yw.get_range(Key("a"))


def test_constructor_checks_node_type():
    with pytest.raises(ValueError):
        YAMLWhereSequence(None)
