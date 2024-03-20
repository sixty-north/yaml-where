"""Basic types for representing positions and ranges in a document."""

from dataclasses import dataclass


@dataclass
class Position:
    "Zero-based indexes describing a position in a document."
    line: int
    column: int


@dataclass
class Range:
    "Half-open range describing a span inside a document."
    start: Position
    end: Position
