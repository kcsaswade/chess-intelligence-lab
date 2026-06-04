from chesslab.engine.board import coord_to_index
from chesslab.engine.legal_moves import generate_legal_moves
from chesslab.io.fen import parse_fen


def test_only_check_responses_remain() -> None:
    position = parse_fen("4r3/8/8/8/8/8/8/R3K3 w - - 0 1")
    legal_moves = generate_legal_moves(position)

    legal_pairs = {(move.from_sq, move.to_sq) for move in legal_moves}
    assert (coord_to_index("e1"), coord_to_index("d1")) in legal_pairs
    assert (coord_to_index("e1"), coord_to_index("f1")) in legal_pairs
    assert (coord_to_index("e1"), coord_to_index("d2")) in legal_pairs
    assert (coord_to_index("e1"), coord_to_index("f2")) in legal_pairs

    assert all(from_sq == coord_to_index("e1") for from_sq, _ in legal_pairs)