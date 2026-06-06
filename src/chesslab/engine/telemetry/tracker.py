"""Telemetry-owned mutable tracker used during recursive search."""


from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SearchTracker:
    """Mutable counters for recursive search."""
    nodes: int = 0
    cutoffs: int = 0
    max_depth_reached: int = 0

    def record_node(self, ply: int) -> None:
        self.nodes += 1
        if ply > self.max_depth_reached:
            self.max_depth_reached = ply

    def record_cutoff(self) -> None:
        self.cutoffs += 1