from yaml_where.path import Index, Key, Value
from yaml_where.testing.helpers import clean_yaml
from yaml_where import YAMLWhere


def test_get_seq_in_map():
    yaml = """
    a: [1, 2]
    b:
        c:
            - 4
            - 5
    """
    yw = YAMLWhere.from_string(clean_yaml(yaml))

    r = yw.get_range("a", 0)
    assert yw.get_path(r.start) == (Value('a'), Index(0))

    r = yw.get_range("a", 1)
    assert yw.get_path(r.start) == (Value('a'), Index(1))

    r = yw.get_range("b", "c", 0)
    assert yw.get_path(r.start) == (Value('b'), Value('c'), Index(0))

    r = yw.get_range("b", "c", 1)
    assert yw.get_path(r.start) == (Value('b'), Value('c'), Index(1))


def test_get_map_in_seq():
    yaml = """
    - a: 1
      b: 2
    - [{c: 3}]
    """
    yw = YAMLWhere.from_string(clean_yaml(yaml))

    r = yw.get_range(0, "a")
    assert yw.get_path(r.start) == (Index(0), Value('a'))

    r = yw.get_range(0, "b")
    assert yw.get_path(r.start) == (Index(0), Value('b'))

    r = yw.get_range(1, 0, "c")
    assert yw.get_path(r.start) == (Index(1), Index(0), Value('c'))


def test_get_key_map_in_seq():
    yaml = """
    - a: 1
      b: 2
    - [{c: 3}]
    """
    yw = YAMLWhere.from_string(clean_yaml(yaml))

    r = yw.get_key_range(0, "a")
    assert yw.get_path(r.start) == (Index(0), Key('a'))

    r = yw.get_key_range(0, "b")
    assert yw.get_path(r.start) == (Index(0), Key('b'))

    r = yw.get_key_range(1, 0, "c")
    assert yw.get_path(r.start) == (Index(1), Index(0), Key('c'))


def test_get_value_seq_in_map():
    yaml = """
    a: [1, 2]
    b:
        c:
            - 4
            - 5
    """
    yw = YAMLWhere.from_string(clean_yaml(yaml))

    r = yw.get_value_range("a", 0)
    assert yw.get_path(r.start) == (Value('a'), Index(0))

    r = yw.get_value_range("a", 1)
    assert yw.get_path(r.start) == (Value('a'), Index(1))

    r = yw.get_value_range("b", "c", 0)
    assert yw.get_path(r.start) == (Value('b'), Value('c'), Index(0))

    r = yw.get_value_range("b", "c", 1)
    assert yw.get_path(r.start) == (Value('b'), Value('c'), Index(1))


def test_get_value_map_in_seq():
    yaml = """
    - a: 1
      b: 2
    - [{c: 3}]
    """
    yw = YAMLWhere.from_string(clean_yaml(yaml))

    r = yw.get_value_range(0, "a")
    assert yw.get_path(r.start) == (Index(0), Value('a'))

    r = yw.get_value_range(0, "b")
    assert yw.get_path(r.start) == (Index(0), Value('b'))

    r = yw.get_value_range(1, 0, "c")
    assert yw.get_path(r.start) == (Index(1), Index(0), Value('c'))
