from chesslab.engine.legal_moves import generate_legal_moves
from chesslab.engine.search.ordering import order_moves
from chesslab.io.fen import parse_fen


def test_captures_before_quiets() -> None:
    position = parse_fen("4k3/8/8/3p4/4P3/8/8/4K3 w - - 0 1")
    ordered = order_moves(position, generate_legal_moves(position))
    capture_indices = [i for i, move in enumerate(ordered) if move.is_capture]
    quiet_indices = [i for i, move in enumerate(ordered) if not move.is_capture]
    assert capture_indices
    assert quiet_indices
    assert max(capture_indices) < min(quiet_indices)


def test_ordering_is_deterministic() -> None:
    position = parse_fen("4k3/8/8/3p4/4P3/8/8/4K3 w - - 0 1")
    moves = generate_legal_moves(position)
    first = order_moves(position, moves)
    second = order_moves(position, moves)
    assert first == second