from chesslab.engine.board import coord_to_index, index_to_coord
from chesslab.engine.move_generation.slider_moves import generate_rook_moves
from chesslab.io.fen import parse_fen


def test_slider_stops_at_own_piece_and_after_capture() -> None:
    position = parse_fen("8/8/8/4p3/2P1R3/8/8/8 w - - 0 1")
    moves = generate_rook_moves(position, coord_to_index("e4"))
    coords = {index_to_coord(move.to_sq) for move in moves}
    assert "c4" not in coords
    assert "e5" in coords
    assert "e6" not in coords