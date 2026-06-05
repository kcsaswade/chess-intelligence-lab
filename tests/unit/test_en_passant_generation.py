from chesslab.engine.board import coord_to_index
from chesslab.engine.legal_moves import generate_legal_moves
from chesslab.io.fen import parse_fen


def test_en_passant_generated_when_target_exists() -> None:
    position = parse_fen("4k3/8/8/3pP3/8/8/8/4K3 w - d6 0 1")
    moves = generate_legal_moves(position)
    assert any(
        move.from_sq == coord_to_index("e5")
        and move.to_sq == coord_to_index("d6")
        and move.is_en_passant
        for move in moves
    )