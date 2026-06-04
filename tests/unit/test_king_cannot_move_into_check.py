from chesslab.engine.board import coord_to_index
from chesslab.engine.legal_moves import generate_legal_moves
from chesslab.io.fen import parse_fen


def test_king_cannot_move_into_attacked_square() -> None:
    position = parse_fen("4k3/8/8/8/8/8/3r4/4K3 w - - 0 1")
    legal_moves = generate_legal_moves(position)
    destinations = {move.to_sq for move in legal_moves if move.from_sq == coord_to_index("e1")}

    assert coord_to_index("f2") not in destinations