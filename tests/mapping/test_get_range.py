import pytest
from yaml_where.path import Item, Key, Value
from yaml_where.range import Range
from yaml_where.yaml_where import YAMLWhereMapping
from yaml_where.testing.helpers import clean_yaml
from yaml_where import YAMLWhere
from yaml_where.exceptions import MissingKeyError, UndefinedAccessError


class TestTopLevel:
    source_map = YAMLWhere.from_string("a: 1\nb: 42")

    def test_item_1(self):
        assert self.source_map.get_range(Item("a")) == Range.from_parts(0, 0, 0, 4)

    def test_item_2(self):
        assert self.source_map.get_range(Item("b")) == Range.from_parts(1, 0, 1, 5)

    def test_key_1(self):
        assert self.source_map.get_range(Key("a")) == Range.from_parts(0, 0, 0, 1)

    def test_key_2(self):
        assert self.source_map.get_range(Key("b")) == Range.from_parts(1, 0, 1, 1)

    def test_value_1(self):
        assert self.source_map.get_range(Value("a")) == Range.from_parts(0, 3, 0, 4)

    def test_value_2(self):
        assert self.source_map.get_range(Value("b")) == Range.from_parts(1, 3, 1, 5)


def test_nested():
    yaml = """
    a:
        b: 42
        c:
            d: hola
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    assert source_map.get_range(Value("a"), Item("b")) == Range.from_parts(1, 4, 1, 9)


def test_key_top_level():
    source_map = YAMLWhere.from_string("a: 1\nbb: 42")
    assert source_map.get_range(Key("a")) == Range.from_parts(0, 0, 0, 1)
    # assert source_map.get_range("bb") == Range.from_parts(1, 0, 1, 2)


def test_top_level_missing_key():
    source_map = YAMLWhere.from_string("a: 1\nb: 42")
    with pytest.raises(MissingKeyError):
        source_map.get_range(Item("c"))


def test_nested_missing_key():
    yaml = """
    a:
        b: 42
        c:
            d: hola
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))
    with pytest.raises(MissingKeyError):
        source_map.get_range(Key("a"), Key("e"))


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
        source_map.get_range()
