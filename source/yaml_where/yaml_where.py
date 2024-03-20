from ruamel.yaml import YAML, MappingNode, Node, SequenceNode, ScalarNode
from yaml_where.range import Position, Range


class YAMLWhere:
    @classmethod
    def from_string(cls, source: str):
        y = YAML(typ="rt")
        node = y.compose(source)
        return cls(node)

    def __init__(self, node: Node):
        self.node = node

    def get(self, *keys: str | int) -> Range:
        """Get the range for an entire entry.

        If the final key/index is into a sequence, this gets the extents of the sequence entry. If it's into a
        mapping, this gets the extents of the key and value combined.

        Raises:
            KeyError: If the key is not found.
            ValueError: If this is called with zero arguments on a non-scalar YAML document.
        """
        if not keys:
            if isinstance(self.node, ScalarNode):
                return Range(
                    Position(self.node.start_mark.line, self.node.start_mark.column),
                    Position(self.node.end_mark.line, self.node.end_mark.column),
                )
            raise ValueError("get() with no arguments is not defined for non-scalar nodes")

        return self._get(keys[0], *keys[1:])

    def _get(self, key: str | int, *keys: str | int) -> Range:
        """Get the range for an entire entry.

        If the final key/index is into a sequence, this gets the extents of the sequence entry. If it's into a
        mapping, this gets the extents of the key and value combined.

        Raises:
            KeyError: If the key is not found.
        """
        if isinstance(self.node, MappingNode):
            for child_key, child_value in self.node.value:
                if child_key.value == key:
                    if not keys:
                        return Range(
                            Position(child_key.start_mark.line, child_key.start_mark.column),
                            Position(child_value.end_mark.line, child_value.end_mark.column),
                        )
                    else:
                        return YAMLWhere(child_value).get(*keys)
        elif isinstance(self.node, SequenceNode):
            if isinstance(key, int):
                if key < len(self.node.value):
                    if not keys:
                        value_node = self.node.value[key]
                        return Range(
                            Position(value_node.start_mark.line, value_node.start_mark.column),
                            Position(value_node.end_mark.line, value_node.end_mark.column),
                        )
                    else:
                        return YAMLWhere(self.node.value[key]).get(*keys)

        raise KeyError(key)

    def get_key(self, key: str | int, *keys: str | int) -> Range:
        """Get the range for a mapping key.

        Raises:
            KeyError: If the key is not found.
        """
        if isinstance(self.node, MappingNode):
            for child_key, child_value in self.node.value:
                if child_key.value == key:
                    if not keys:
                        return Range(
                            Position(child_key.start_mark.line, child_key.start_mark.column),
                            Position(child_key.end_mark.line, child_key.end_mark.column),
                        )
                    else:
                        return YAMLWhere(child_value).get_key(*keys)
        elif isinstance(self.node, SequenceNode):
            if not keys:
                raise ValueError("get_key() is not defined for sequence elements")
            return YAMLWhere(self.node.value[key]).get_key(*keys)

        raise KeyError(key)

    def get_value(self, key: str | int, *keys: str | int) -> Range:
        """Get the range for a mapping value.

        Raises:
            KeyError: If the key is not found.
        """
        if isinstance(self.node, MappingNode):
            for child_key, child_value in self.node.value:
                if child_key.value == key:
                    if not keys:
                        return Range(
                            Position(child_value.start_mark.line, child_value.start_mark.column),
                            Position(child_value.end_mark.line, child_value.end_mark.column),
                        )
                    else:
                        return YAMLWhere(child_value).get_value(*keys)
        elif isinstance(self.node, SequenceNode):
            if isinstance(key, int):
                if key < len(self.node.value):
                    if not keys:
                        value_node = self.node.value[key]
                        return Range(
                            Position(value_node.start_mark.line, value_node.start_mark.column),
                            Position(value_node.end_mark.line, value_node.end_mark.column),
                        )
                    else:
                        return YAMLWhere(self.node.value[key]).get_value(*keys)

        raise KeyError(key)
