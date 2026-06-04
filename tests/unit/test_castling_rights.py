from chesslab.engine.castling import CastlingRights


def test_parse_all_castling_rights() -> None:
    rights = CastlingRights.from_fen_field("KQkq")
    assert rights.white_kingside is True
    assert rights.white_queenside is True
    assert rights.black_kingside is True
    assert rights.black_queenside is True


def test_parse_no_castling_rights() -> None:
    rights = CastlingRights.from_fen_field("-")
    assert rights.to_fen_field() == "-"


def test_serialize_mixed_castling_rights() -> None:
    rights = CastlingRights(white_kingside=True, black_queenside=True)
    assert rights.to_fen_field() == "Kq"