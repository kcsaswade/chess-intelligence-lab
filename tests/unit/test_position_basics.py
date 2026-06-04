from chesslab.engine.castling import CastlingRights
from chesslab.engine.piece import Color, Piece, PieceType
from chesslab.engine.position import Position


def test_position_stores_all_fields() -> None:
    board = [None] * 64
    piece = Piece(Color.WHITE, PieceType.KING)
    board[0] = piece

    position = Position(
        board=board,
        side_to_move=Color.BLACK,
        castling_rights=CastlingRights(white_kingside=True),
        en_passant_square=20,
        halfmove_clock=7,
        fullmove_number=12,
    )

    assert len(position.board) == 64
    assert position.side_to_move is Color.BLACK
    assert position.castling_rights.white_kingside is True
    assert position.en_passant_square == 20
    assert position.halfmove_clock == 7
    assert position.fullmove_number == 12
    assert position.piece_at(0) == piece


def test_set_piece_updates_board() -> None:
    position = Position()
    piece = Piece(Color.BLACK, PieceType.QUEEN)

    position.set_piece(10, piece)

    assert position.piece_at(10) == piece