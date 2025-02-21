import pytest
from yaml_where import YAMLWhere
from yaml_where.exceptions import NoSuchPathError
from yaml_where.path import Key, Value
from yaml_where.testing.helpers import clean_yaml


def test_top_level():
    source_map = YAMLWhere.from_string("a: 1\nb: 42")

    r = source_map.get_key("a")
    assert list(source_map.get_path(r.start)) == [Key("a")]

    r = source_map.get_value("a")
    assert list(source_map.get_path(r.start)) == [Value("a")]

    r = source_map.get_key("b")
    assert list(source_map.get_path(r.start)) == [Key("b")]

    r = source_map.get_value("b")
    assert list(source_map.get_path(r.start)) == [Value("b")]


def test_nested():
    yaml = """
    a:
        b: 42
        c:
            d: hola
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))

    r = source_map.get_key("a", "b")
    assert list(source_map.get_path(r.start)) == [Value("a"), Key("b")]

    r = source_map.get_value("a", "b")
    assert list(source_map.get_path(r.start)) == [Value("a"), Value("b")]

    r = source_map.get_key("a", "c")
    assert list(source_map.get_path(r.start)) == [Value("a"), Key("c")]

    # Interesting that we can't really distinguish between the value of 'c' and the key of 'd'.
    r = source_map.get_value("a", "c")
    assert list(source_map.get_path(r.start)) == [Value("a"), Value("c"), Key("d")]

    r = source_map.get_key("a", "c", "d")
    assert list(source_map.get_path(r.start)) == [Value("a"), Value("c"), Key("d")]

    r = source_map.get_value("a", "c", "d")
    assert list(source_map.get_path(r.start)) == [Value("a"), Value("c"), Value("d")]


def test_not_found():
    yaml = """
    a:
        b: 42
        c:
            d: hola
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))

    r = source_map.get_value("a", "c", "d")

    with pytest.raises(NoSuchPathError):
        list(source_map.get_path(r.end))
