from yaml_where.range import Position
from yaml_where.yaml_where import YAMLWhere


def test_entire_document():
    yaml = "hello"
    source_map = YAMLWhere.from_string(yaml)
    assert list(source_map.get_path(Position(1, 1))) == []
