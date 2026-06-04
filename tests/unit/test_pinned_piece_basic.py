from chesslab.engine.board import coord_to_index
from chesslab.engine.legal_moves import generate_legal_moves
from chesslab.io.fen import parse_fen


def test_pinned_rook_cannot_leave_file() -> None:
    position = parse_fen("4r3/8/8/8/8/8/4R3/4K3 w - - 0 1")
    legal_moves = generate_legal_moves(position)

    rook_moves = [move for move in legal_moves if move.from_sq == coord_to_index("e2")]
    destinations = {move.to_sq for move in rook_moves}

    assert coord_to_index("f2") not in destinations
    assert coord_to_index("d2") not in destinations
    assert coord_to_index("e3") in destinations