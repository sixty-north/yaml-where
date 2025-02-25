from yaml_where.path import Index, Item, Value
from yaml_where.testing.helpers import clean_yaml, extent
from yaml_where import YAMLWhere


class TestGetSeqInMap:
    yaml = """
    a: [1, 2]
    b:
        c:
            - 4
            - 5
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))

    def test_1(self):
        assert self.source_map.get_range(Value("a"), Index(0)) == extent(0, 4, 1)

    def test_2(self):
        assert self.source_map.get_range(Value("a"), Index(1)) == extent(0, 7, 1)

    def test_3(self):
        assert self.source_map.get_range(Value("b"), Value("c"), Index(0)) == extent(3, 10, 1)

    def test_4(self):
        assert self.source_map.get_range(Value("b"), Value("c"), Index(1)) == extent(4, 10, 1)


class TestGetMapInSeq:
    yaml = """
    - a: 1
      b: 2
    - [{c: 3}]
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))

    def test_1(self):
        assert self.source_map.get_range(Index(0), Item("a")) == extent(0, 2, 4)

    def test_2(self):
        assert self.source_map.get_range(Index(0), Item("b")) == extent(1, 2, 4)

    def test_3(self):
        assert self.source_map.get_range(Index(1), Index(0), Item("c")) == extent(2, 4, 4)
