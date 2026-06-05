"""Perft and divide for legal move tree validation."""

from __future__ import annotations

from chesslab.engine.legal_moves import generate_legal_moves
from chesslab.engine.make_unmake import make_move, unmake_move
from chesslab.engine.move import Move
from chesslab.engine.position import Position


def perft(position: Position, depth: int) -> int:
    """Count legal leaf nodes at a fixed depth."""
    if depth < 0:
        raise ValueError("depth must be non-negative")
    if depth == 0:
        return 1

    nodes = 0
    moves = generate_legal_moves(position)
    for move in moves:
        undo = make_move(position, move)
        try:
            nodes += perft(position, depth - 1)
        finally:
            unmake_move(position, move, undo)
    return nodes


def divide(position: Position, depth: int) -> list[tuple[Move, int]]:
    """Return per-root-move perft counts."""
    if depth < 1:
        raise ValueError("depth must be at least 1 for divide")

    results: list[tuple[Move, int]] = []
    moves = generate_legal_moves(position)
    for move in moves:
        undo = make_move(position, move)
        try:
            child_nodes = perft(position, depth - 1)
        finally:
            unmake_move(position, move, undo)
        results.append((move, child_nodes))
    return results