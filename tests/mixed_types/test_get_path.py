from yaml_where.path import Index, Key, Value
from yaml_where.testing.helpers import clean_yaml
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
        r = self.source_map.get_range(Value("a"), Index(0))
        assert self.source_map.get_path(r.start) == (Value('a'), Index(0))

    def test_2(self):
        r = self.source_map.get_range(Value("a"), Index(1))
        assert self.source_map.get_path(r.start) == (Value('a'), Index(1))

    def test_3(self):
        r = self.source_map.get_range(Value("b"), Value("c"), Index(0))
        assert self.source_map.get_path(r.start) == (Value('b'), Value('c'), Index(0))

    def test_4(self):
        r = self.source_map.get_range(Value("b"), Value("c"), Index(1))
        assert self.source_map.get_path(r.start) == (Value('b'), Value('c'), Index(1))


class TestGetMapInSeq:
    yaml = """
    - a: 1
      b: 2
    - [{c: 3}]
    """
    source_map = YAMLWhere.from_string(clean_yaml(yaml))

    def test_1(self):
        r = self.source_map.get_range(Index(0), Value("a"))
        assert self.source_map.get_path(r.start) == (Index(0), Value('a'))

    def test_2(self):
        r = self.source_map.get_range(Index(0), Value("b"))
        assert self.source_map.get_path(r.start) == (Index(0), Value('b'))

    def test_3(self):
        r = self.source_map.get_range(Index(1), Index(0), Value("c"))
        assert self.source_map.get_path(r.start) == (Index(1), Index(0), Value('c'))

