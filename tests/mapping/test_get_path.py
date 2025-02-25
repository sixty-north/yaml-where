import pytest
from yaml_where import YAMLWhere
from yaml_where.exceptions import NoSuchPathError
from yaml_where.path import Item, Key, Value
from yaml_where.testing.helpers import clean_yaml


class TestTopLevel:
    source_map = YAMLWhere.from_string("a: 1\nb: 42")


    def test_1(self):
        r = self.source_map.get_range(Key("a"))
        assert self.source_map.get_path(r.start) == (Key("a"),)


    def test_2(self):
        r = self.source_map.get_range(Value("a"))
        assert self.source_map.get_path(r.start) == (Value("a"),)


    def test_3(self):
        r = self.source_map.get_range(Key("b"))
        assert self.source_map.get_path(r.start) == (Key("b"),)


    def test_4(self):
        r = self.source_map.get_range(Value("b"))
        assert self.source_map.get_path(r.start) == (Value("b"),)


class TestNested:
    yaml = """
    a:
        b: 42
        c:
            d: hola
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))


    def test_nested_1(self):
        r = self.source_map.get_range(Value("a"), Key("b"))
        assert self.source_map.get_path(r.start) == (Value("a"), Key("b"))


    def test_nested_2(self):
        r = self.source_map.get_range(Value("a"), Value("b"))
        assert self.source_map.get_path(r.start) == (Value("a"), Value("b"))


    def test_nested_3(self):
        r = self.source_map.get_range(Value("a"), Key("c"))
        assert self.source_map.get_path(r.start) == (Value("a"), Key("c"))


    def test_nested_4(self):
        r = self.source_map.get_range(Value("a"), Value("c"))
        assert self.source_map.get_path(r.start) == (Value("a"), Value("c"), Key("d"))


    def test_nested_5(self):
        r = self.source_map.get_range(Value("a"), Value("c"), Key("d"))
        assert self.source_map.get_path(r.start) == (
            Value("a"),
            Value("c"),
            Key("d"),
        )


    def test_nested_6(self):
        r = self.source_map.get_range(Value("a"), Value("c"), Value("d"))
        assert self.source_map.get_path(r.start) == (
            Value("a"),
            Value("c"),
            Value("d"),
        )


    def test_nested_7(self):
        r = self.source_map.get_range(Item("a"))
        assert self.source_map.get_path(r.start) == (Key("a"),)


    def test_nested_8(self):
        r = self.source_map.get_range(Value("a"), Item("c"))
        assert self.source_map.get_path(r.start) == (
            Value("a"),
            Key("c"),
        )


    def test_nested_9(self):
        r = self.source_map.get_range(Value("a"), Value("c"), Item("d"))
        assert self.source_map.get_path(r.start) == (
            Value("a"),
            Key("c"),
            Key("d"),
        )


    def test_nested_10(self):
        r = self.source_map.get_range(Item("a"), Item("c"), Item("d"))
        assert self.source_map.get_path(r.start) == (
            Value("a"),
            Key("c"),
            Key("d"),
        )


def test_not_found():
    yaml = """
    a:
        b: 42
        c:
            d: hola
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))

    r = source_map.get_range(Value("a"), Value("c"), Value("d"))

    with pytest.raises(NoSuchPathError):
        source_map.get_path(r.end)
