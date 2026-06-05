"""Principal variation helpers."""


from __future__ import annotations

from chesslab.engine.move import Move


def prepend_pv(move: Move, child_pv: list[Move]) -> list[Move]:
    """Build a PV by prepending the current best move to the child PV."""
    return [move, *child_pv]