from chesslab.engine.board import coord_to_index
from chesslab.engine.move_generation.slider_moves import (
    generate_bishop_moves,
    generate_queen_moves,
    generate_rook_moves,
)
from chesslab.io.fen import parse_fen


def test_queen_is_rook_plus_bishop_on_empty_board() -> None:
    position = parse_fen("8/8/8/8/4Q3/8/8/8 w - - 0 1")
    queen_moves = generate_queen_moves(position, coord_to_index("e4"))
    rook_moves = generate_rook_moves(position, coord_to_index("e4"))
    bishop_moves = generate_bishop_moves(position, coord_to_index("e4"))
    assert len(queen_moves) == len(rook_moves) + len(bishop_moves)