from chesslab.engine.board import coord_to_index, index_to_coord
from chesslab.engine.move_generation.slider_moves import generate_bishop_moves
from chesslab.io.fen import parse_fen


def _coords(moves: list) -> set[str]:
    return {index_to_coord(move.to_sq) for move in moves}


def test_bishop_center_empty_board() -> None:
    position = parse_fen("8/8/8/8/3B4/8/8/8 w - - 0 1")
    moves = generate_bishop_moves(position, coord_to_index("d4"))
    assert len(moves) == 13
    assert "a1" in _coords(moves)
    assert "g7" in _coords(moves)


def test_bishop_blockers_and_capture() -> None:
    position = parse_fen("8/6p1/8/5P2/3B4/8/1P6/8 w - - 0 1")
    moves = generate_bishop_moves(position, coord_to_index("d4"))
    coords = _coords(moves)
    assert "b2" not in coords
    assert "g7" in coords
    assert "h8" not in coords