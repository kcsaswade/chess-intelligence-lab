from chesslab.engine.piece import Color, Piece, PieceType


def test_piece_creation() -> None:
    piece = Piece(color=Color.WHITE, kind=PieceType.QUEEN)
    assert piece.color is Color.WHITE
    assert piece.kind is PieceType.QUEEN


def test_piece_equality() -> None:
    a = Piece(color=Color.BLACK, kind=PieceType.KNIGHT)
    b = Piece(color=Color.BLACK, kind=PieceType.KNIGHT)
    assert a == b


def test_piece_from_fen_char_white() -> None:
    piece = Piece.from_fen_char("N")
    assert piece.color is Color.WHITE
    assert piece.kind is PieceType.KNIGHT


def test_piece_from_fen_char_black() -> None:
    piece = Piece.from_fen_char("q")
    assert piece.color is Color.BLACK
    assert piece.kind is PieceType.QUEEN


def test_piece_to_fen_char() -> None:
    assert Piece(Color.WHITE, PieceType.ROOK).to_fen_char() == "R"
    assert Piece(Color.BLACK, PieceType.BISHOP).to_fen_char() == "b"