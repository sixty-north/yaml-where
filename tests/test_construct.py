from yaml_where import YAMLWhere


def test_from_empty_source():
    YAMLWhere.from_string("")


def test_from_simple_dict():
    YAMLWhere.from_string("a: 1\nb: 2")
