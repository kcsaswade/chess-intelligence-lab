from chesslab.engine.board import coord_to_index, index_to_coord
from chesslab.engine.move_generation.pawn_moves import generate_pawn_moves
from chesslab.engine.piece import PieceType
from chesslab.io.fen import parse_fen


def test_white_pawn_promotion_pushes() -> None:
    position = parse_fen("8/4P3/8/8/8/8/8/8 w - - 0 1")
    moves = generate_pawn_moves(position, coord_to_index("e7"))
    promotions = {move.promotion for move in moves if index_to_coord(move.to_sq) == "e8"}
    assert promotions == {
        PieceType.QUEEN,
        PieceType.ROOK,
        PieceType.BISHOP,
        PieceType.KNIGHT,
    }


def test_black_pawn_promotion_pushes() -> None:
    position = parse_fen("8/8/8/8/8/8/4p3/8 b - - 0 1")
    moves = generate_pawn_moves(position, coord_to_index("e2"))
    promotions = {move.promotion for move in moves if index_to_coord(move.to_sq) == "e1"}
    assert promotions == {
        PieceType.QUEEN,
        PieceType.ROOK,
        PieceType.BISHOP,
        PieceType.KNIGHT,
    }


def test_white_pawn_promotion_captures() -> None:
    position = parse_fen("3r1n2/4P3/8/8/8/8/8/8 w - - 0 1")
    moves = generate_pawn_moves(position, coord_to_index("e7"))
    capture_promotions = [move for move in moves if move.is_capture]
    assert len(capture_promotions) == 8