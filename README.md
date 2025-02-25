# YAML Where?

`yaml_where` calculates source maps for YAML files, allowing you to correlate file locations with elements in
YAML documents.

![CI](https://github.com/sixty-north/yaml-where/actions/workflows/actions.yml/badge.svg)

## Installation

    $ pip install yaml-where


## Examples

### Mappings

Find the range containing the key and value of a map entry:

```python
source_map = YAMLWhere.from_string("a: 1\nb: 42")
assert source_map.get_range(Item("b")) == Range(Position(1, 0), Position(1, 5))
```

Or get the range of just the key:
```python
source_map = YAMLWhere.from_string("a: 1\nb: 42")
assert source_map.get_range(Key("a")) == Range(Position(0, 0), Position(0, 1))
```

Or just the value:
```python
source_map = YAMLWhere.from_string("a: 1\nb: 42")
assert source_map.get_range(Value("b")) == Range(Position(1, 3), Position(1, 5))
```

You can also look up nested locations:
```python
yaml = """a:
    b: 42
    c:
        doo: hola
"""
source_map = YAMLWhere.from_string(yaml)
assert source_map.get_range(Value("a"), Key("b")) == Range(Position(1, 4), Position(1, 5))
assert source_map.get_range(Value("a"), Key("c")) == Range(Position(2, 4), Position(2, 5))
assert source_map.get_range(Value("a"), Value("c"), Key("doo")) == Range(Position(3, 8), Position(3, 11))
```

### Sequences

You can also find ranges for sequence elements:
```python
yaml = """[1,
 a, foo,
 
     indented]
"""
source_map = YAMLWhere.from_string(yaml)
assert source_map.get_range(Index(0)) == Range(Position(0, 1), Position(0, 2))
assert source_map.get_range(Index(1)) == Range(Position(1, 1), Position(1, 2))
assert source_map.get_range(Index(2)) == Range(Position(1, 4), Position(1, 7))
assert source_map.get_range(Index(3)) == Range(Position(3, 5), Position(3, 13))
```

## CI/CD

Tests will be run on every push to Github.

Use the "bump-and-publish" job in Github Actions to make new releases.