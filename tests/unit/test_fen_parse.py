from chesslab.engine.piece import Color, PieceType
from chesslab.io.fen import parse_fen


def test_parse_start_position() -> None:
    pos = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    assert pos.side_to_move is Color.WHITE
    assert pos.castling_rights.to_fen_field() == "KQkq"
    assert pos.en_passant_square is None
    assert pos.halfmove_clock == 0
    assert pos.fullmove_number == 1


def test_parse_empty_board() -> None:
    pos = parse_fen("8/8/8/8/8/8/8/8 w - - 0 1")
    assert all(piece is None for piece in pos.board)


def test_parse_position_with_en_passant() -> None:
    pos = parse_fen("8/8/8/3pP3/8/8/8/8 w - d6 0 2")
    assert pos.en_passant_square is not None


def test_parse_position_with_move_counters() -> None:
    pos = parse_fen("8/8/8/8/8/8/8/8 b - - 17 42")
    assert pos.side_to_move is Color.BLACK
    assert pos.halfmove_clock == 17
    assert pos.fullmove_number == 42


def test_parse_specific_piece_locations() -> None:
    pos = parse_fen("8/8/8/8/4k3/8/8/4K3 w - - 0 1")
    assert pos.piece_at(4) is not None
    assert pos.piece_at(4).kind is PieceType.KING
    assert pos.piece_at(28) is not None
    assert pos.piece_at(28).kind is PieceType.KING