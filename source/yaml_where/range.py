"""Basic types for representing positions and ranges in a document."""

from dataclasses import dataclass
from ruamel.yaml.nodes import Node


@dataclass
class Position:
    "Zero-based indexes describing a position in a document."
    line: int
    column: int

    def __le__(self, other):
        "Check if this position is before or at the same location as another."
        return (self.line <= other.line) or (self.line == other.line and self.column <= other.column)


@dataclass
class Range:
    "Half-open range describing a span inside a document."
    start: Position
    end: Position


    def __le__(self, other):
        "Check if this range is contained within another."
        return other.start <= self.start and self.end <= other.end

    @classmethod
    def beginning(cls, length=1):
        "Create a range that starts at the beginning of the document."
        return cls(Position(0, 0), Position(0, length))

    # TODO: There are places where we could use this that are currently explicitly creating
    # Ranges from Nodes.
    @classmethod
    def from_node(cls, node: Node):
        "Create a range that covers the entire node."
        return cls(
            Position(node.start_mark.line, node.start_mark.column),
            Position(node.end_mark.line, node.end_mark.column),
        )

    @classmethod
    def from_parts(cls, start_line, start_column, end_line, end_column):
        "Create a range from its parts."
        return cls(Position(start_line, start_column), Position(end_line, end_column))