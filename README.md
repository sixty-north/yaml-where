# YAML Where?

`yaml_where` calculates source maps for YAML files, allowing you to correlate file locations with elements in
YAML documents.

![CI](https://github.com/sixty-north/yaml-where/actions/workflows/actions.yml/badge.svg)

## Installation

    $ pip install yaml-where


## Examples

### Mappings

Find the range containg the the key and value of a map entry:

```python
source_map = YAMLWhere.from_string("a: 1\nb: 42")
assert source_map.get("b") == Range(Position(1, 0), Position(1, 5))
```

Or get the range of just the key:
```python
source_map = YAMLWhere.from_string("a: 1\nb: 42")
assert source_map.get_key("a") == Range(Position(0, 0), Position(0, 1))
```

Or just the value:
```python
source_map = YAMLWhere.from_string("a: 1\nbb: 42")
assert source_map.get_value("bb") == Range(Position(1, 4), Position(1, 6))
```

You can also look up nested locations:
```python
yaml = """a:
    b: 42
    c:
        doo: hola
"""
source_map = YAMLWhere.from_string(yaml)
assert source_map.get_key("a", "b") == Range(Position(1, 4), Position(1, 5))
assert source_map.get_key("a", "c") == Range(Position(2, 4), Position(2, 5))
assert source_map.get_key("a", "c", "doo") == Range(Position(3, 8), Position(3, 11))
```

### Sequences

You can also find ranges for sequence elements:
```python
yaml = """[1,
 a, foo,
 
     indented]
"""
source_map = YAMLWhere.from_string(yaml)
assert source_map.get(0) == Range(Position(0, 1), Position(0, 2))
assert source_map.get(1) == Range(Position(1, 1), Position(1, 2))
assert source_map.get(2) == Range(Position(1, 4), Position(1, 7))
assert source_map.get(3) == Range(Position(3, 5), Position(3, 13))
```

## CI/CD

Bump the version like this:

```
$ bumpversion patch
$ git push --follow-tags
```
