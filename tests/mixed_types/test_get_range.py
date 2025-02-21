from yaml_where.testing.helpers import clean_yaml, extent
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
    assert yw.get_range("a", 0) == extent(0, 4, 1)
    assert yw.get_range("a", 1) == extent(0, 7, 1)
    assert yw.get_range("b", "c", 0) == extent(3, 10, 1)
    assert yw.get_range("b", "c", 1) == extent(4, 10, 1)


def test_get_map_in_seq():
    yaml = """
    - a: 1
      b: 2
    - [{c: 3}]
    """
    yw = YAMLWhere.from_string(clean_yaml(yaml))
    assert yw.get_range(0, "a") == extent(0, 2, 4)
    assert yw.get_range(0, "b") == extent(1, 2, 4)
    assert yw.get_range(1, 0, "c") == extent(2, 4, 4)


def test_get_key_map_in_seq():
    yaml = """
    - a: 1
      b: 2
    - [{c: 3}]
    """
    yw = YAMLWhere.from_string(clean_yaml(yaml))
    assert yw.get_key_range(0, "a") == extent(0, 2, 1)
    assert yw.get_key_range(0, "b") == extent(1, 2, 1)
    assert yw.get_key_range(1, 0, "c") == extent(2, 4, 1)


def test_get_value_seq_in_map():
    yaml = """
    a: [1, 2]
    b:
        c:
            - 4
            - 5
    """
    yw = YAMLWhere.from_string(clean_yaml(yaml))
    assert yw.get_value_range("a", 0) == extent(0, 4, 1)
    assert yw.get_value_range("a", 1) == extent(0, 7, 1)
    assert yw.get_value_range("b", "c", 0) == extent(3, 10, 1)
    assert yw.get_value_range("b", "c", 1) == extent(4, 10, 1)


def test_get_value_map_in_seq():
    yaml = """
    - a: 1
      b: 2
    - [{c: 3}]
    """
    yw = YAMLWhere.from_string(clean_yaml(yaml))
    assert yw.get_value_range(0, "a") == extent(0, 5, 1)
    assert yw.get_value_range(0, "b") == extent(1, 5, 1)
    assert yw.get_value_range(1, 0, "c") == extent(2, 7, 1)
