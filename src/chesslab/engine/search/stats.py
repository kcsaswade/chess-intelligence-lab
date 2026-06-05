"""Structured search statistics."""


from __future__ import annotations

from dataclasses import dataclass, field

from chesslab.engine.move import Move


@dataclass(frozen=True)
class SearchStats:
    """Search statistics returned to callers."""
    nodes: int
    cutoffs: int
    depth_reached: int
    time_ms: float
    principal_variation: list[Move] = field(default_factory=list)