from chesslab.engine.legal_moves import generate_legal_moves
from chesslab.io.fen import parse_fen
from chesslab.io.san import move_to_san


def _find_move(position, from_sq: int, to_sq: int):
    for move in generate_legal_moves(position):
        if move.from_sq == from_sq and move.to_sq == to_sq:
            return move
    raise AssertionError("Expected legal move not found")


def test_san_pawn_push() -> None:
    position = parse_fen("4k3/8/8/8/8/8/4P3/4K3 w - - 0 1")
    move = _find_move(position, 12, 20)
    assert move_to_san(position, move) == "e3"


def test_san_castling_kingside() -> None:
    position = parse_fen("4k2r/8/8/8/8/8/8/4K2R w K - 0 1")
    move = _find_move(position, 4, 6)
    assert move_to_san(position, move) == "O-O"


def test_san_promotion() -> None:
    position = parse_fen("4k3/6P1/8/8/8/8/8/4K3 w - - 0 1")
    move = _find_move(position, 54, 62)
    assert move_to_san(position, move).startswith("g8=")