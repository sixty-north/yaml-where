"""Main implementation of source map calculation.
"""

from abc import ABC, abstractmethod
from functools import singledispatch

from ruamel.yaml import YAML, MappingNode, Node, ScalarNode, SequenceNode
from yaml_where.exceptions import MissingKeyError, UndefinedAccessError, UnsupportedNodeTypeError
from yaml_where.range import Position, Range


class YAMLWhere(ABC):
    """Base class for source map calculators for different YAML data types.

    This defines the interface for all source map calculators, but is itself abstract.
    """

    @classmethod
    def from_string(cls, source: str):
        """Create a YAMLWhere from a YAML string.

        Args:
            source (str): The YAML string to parse.

        Returns:
            YAMLWhere: The YAMLWhere instance with source map information.
        """
        y = YAML(typ="rt")
        node = y.compose(source)
        return _from_node(node)

    def __init__(self, node: Node):
        self.node = node

    @abstractmethod
    def get(self, *keys: str | int) -> Range:
        """Get the range for an entire entry.

        Different subclasses will have different behaviors for this method. Mappings will return the range
        for the key-value pair, while sequences will return the range for the sequence element.

        Raises:
            MissingKeyError: A key is of the appropriate type for an element, but is missing in that elements. For
                example, if an integer index is beyond the end of a sequence element.
            UndefinedAccessError: If a key is of an inappropriate type for an element. For example, if a string is
                used to access a sequence element.
        """

    @abstractmethod
    def get_key(self, key: str | int, *keys: str | int) -> Range:
        """Get the range for a mapping key.

        So for a mapping, this would return the range for the key in the key-value pair.

        Raises:
            MissingKeyError: A key is of the appropriate type for an element, but is missing in that elements. For
                example, if an integer index is beyond the end of a sequence element.
            UndefinedAccessError: If a key is of an inappropriate type for an element. For example, if a string is
                used to access a sequence element. Or if 'key' is no a defined concept for the element.
        """

    @abstractmethod
    def get_value(self, key: str | int, *keys: str | int) -> Range:
        """Get the range for a value.

        For a mapping this gets the range of the value in the key-value pair. For a sequence this gets the range
        of the sequence element (just like get()).

        Raises:
            MissingKeyError: A key is of the appropriate type for an element, but is missing in that elements. For
                example, if an integer index is beyond the end of a sequence element.
            UndefinedAccessError: If a key is of an inappropriate type for an element. For example, if a string is
                used to access a sequence element. Or if 'key' is no a defined concept for the element.
        """



class YAMLWhereScalar(YAMLWhere):
    "Source map calculator for scalar nodes."

    def __init__(self, node: ScalarNode):
        if not isinstance(node, ScalarNode):
            raise ValueError(f"YAMLWhereScalar can not be constructed with a {type(node).__name__}")
        super().__init__(node)

    def get(self, *keys: str | int) -> Range:
        if keys:
            raise UndefinedAccessError("get() with no arguments is not defined for scalar nodes")

        return Range(
            Position(self.node.start_mark.line, self.node.start_mark.column),
            Position(self.node.end_mark.line, self.node.end_mark.column),
        )

    def get_key(self, key: str | int, *keys: str | int) -> Range:
        raise UndefinedAccessError("get_key() is not defined for scalar nodes")

    def get_value(self, key: str | int, *keys: str | int) -> Range:
        raise UndefinedAccessError("get_value() is not defined for scalar nodes")


class YAMLWhereSequence(YAMLWhere):
    "Source map calculator for sequence nodes."

    def __init__(self, node: SequenceNode):
        if not isinstance(node, SequenceNode):
            raise ValueError(
                f"YAMLWhereSequence can not be constructed with a {type(node).__name__}"
            )

        super().__init__(node)

    def get(self, *keys: str | int) -> Range:
        if not keys:
            raise UndefinedAccessError(
                "get() with no arguments is not defined for sequence elements"
            )

        key, keys = keys[0], keys[1:]

        if not isinstance(key, int):
            raise UndefinedAccessError(f"Can not access a sequence with non-integer key {key}")

        if keys:
            return _from_node(self.node.value[key]).get(*keys)

        try:
            value_node = self.node.value[key]
        except IndexError as err:
            raise MissingKeyError(key) from err

        return Range(
            Position(value_node.start_mark.line, value_node.start_mark.column),
            Position(value_node.end_mark.line, value_node.end_mark.column),
        )

    def get_key(self, key: str | int, *keys: str | int) -> Range:
        if not keys:
            raise UndefinedAccessError("get_key() is not defined for sequence elements")

        return _from_node(self.node.value[key]).get_key(*keys)

    def get_value(self, key: str | int, *keys: str | int) -> Range:
        if not isinstance(key, int):
            raise UndefinedAccessError(f"Can not access a sequence with non-integer key {key}")

        if keys:
            return _from_node(self.node.value[key]).get_value(*keys)

        try:
            value_node = self.node.value[key]
        except IndexError as err:
            raise MissingKeyError(key) from err

        return Range(
            Position(value_node.start_mark.line, value_node.start_mark.column),
            Position(value_node.end_mark.line, value_node.end_mark.column),
        )


class YAMLWhereMapping(YAMLWhere):
    "Source map calculator for mapping nodes."

    def __init__(self, node: MappingNode):
        if not isinstance(node, MappingNode):
            raise ValueError(
                f"YAMLWhereMapping can not be constructed with a {type(node).__name__}"
            )

        super().__init__(node)

    def get(self, *keys: str | int) -> Range:
        if not keys:
            raise UndefinedAccessError(
                "get() with no arguments is not defined for sequence elements"
            )

        key, keys = keys[0], keys[1:]

        for child_key, child_value in self.node.value:
            if child_key.value == key:
                if not keys:
                    return Range(
                        Position(child_key.start_mark.line, child_key.start_mark.column),
                        Position(child_value.end_mark.line, child_value.end_mark.column),
                    )
                else:
                    return _from_node(child_value).get(*keys)

        raise MissingKeyError(key)

    def get_key(self, key: str | int, *keys: str | int) -> Range:
        for child_key, child_value in self.node.value:
            if child_key.value == key:
                if not keys:
                    return Range(
                        Position(child_key.start_mark.line, child_key.start_mark.column),
                        Position(child_key.end_mark.line, child_key.end_mark.column),
                    )
                else:
                    return _from_node(child_value).get_key(*keys)

        raise MissingKeyError(key)

    def get_value(self, key: str | int, *keys: str | int) -> Range:
        for child_key, child_value in self.node.value:
            if child_key.value == key:
                if not keys:
                    return Range(
                        Position(child_value.start_mark.line, child_value.start_mark.column),
                        Position(child_value.end_mark.line, child_value.end_mark.column),
                    )
                else:
                    return _from_node(child_value).get_value(*keys)

        raise MissingKeyError(key)


class YAMLWhereNull(YAMLWhere):
    "Source map calculator for null nodes."

    def get(self, *keys: str | int) -> Range:
        raise UndefinedAccessError("get() is not defined for null nodes")

    def get_key(self, key: str | int, *keys: str | int) -> Range:
        raise UndefinedAccessError("get_key() is not defined for null nodes")

    def get_value(self, key: str | int, *keys: str | int) -> Range:
        raise UndefinedAccessError("get_value() is not defined for null nodes")


@singledispatch
def _from_node(node: Node) -> YAMLWhere:
    "Construct a YAMLWhere based on the type of the node."
    raise UnsupportedNodeTypeError(
        f"Unsupported node type {type(node).__name__}"
    )  # pragma: no cover


@_from_node.register(ScalarNode)
def _(node):
    return YAMLWhereScalar(node)


@_from_node.register(MappingNode)
def _(node):
    return YAMLWhereMapping(node)


@_from_node.register(SequenceNode)
def _(node):
    return YAMLWhereSequence(node)


@_from_node.register(type(None))
def _(node):
    return YAMLWhereNull(node)

