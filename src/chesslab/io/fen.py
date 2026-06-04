"""FEN parsing and serialization."""

from __future__ import annotations

from chesslab.constants import START_FEN_FIELD_COUNT
from chesslab.engine.board import coord_to_index, index_to_coord, rank_file_to_index
from chesslab.engine.castling import CastlingRights
from chesslab.engine.piece import Color, Piece
from chesslab.engine.position import Position
from chesslab.errors import FenError, InvalidSquareError


def parse_fen(fen: str) -> Position:
    """Parse a FEN string into a Position."""
    fields = fen.strip().split()
    if len(fields) != START_FEN_FIELD_COUNT:
        raise FenError(
            f"FEN must have exactly {START_FEN_FIELD_COUNT} fields, got {len(fields)}: {fen!r}"
        )

    board_field, side_field, castling_field, ep_field, halfmove_field, fullmove_field = fields

    board = _parse_board_field(board_field)
    side_to_move = _parse_side_field(side_field)
    castling_rights = CastlingRights.from_fen_field(castling_field)
    en_passant_square = _parse_en_passant_field(ep_field)
    halfmove_clock = _parse_halfmove_field(halfmove_field)
    fullmove_number = _parse_fullmove_field(fullmove_field)

    return Position(
        board=board,
        side_to_move=side_to_move,
        castling_rights=castling_rights,
        en_passant_square=en_passant_square,
        halfmove_clock=halfmove_clock,
        fullmove_number=fullmove_number,
    )


def to_fen(position: Position) -> str:
    """Serialize a Position to a FEN string."""
    board_field = _serialize_board_field(position)
    side_field = position.side_to_move.value
    castling_field = position.castling_rights.to_fen_field()
    ep_field = (
        "-"
        if position.en_passant_square is None
        else index_to_coord(position.en_passant_square)
    )
    return (
        f"{board_field} {side_field} {castling_field} {ep_field} "
        f"{position.halfmove_clock} {position.fullmove_number}"
    )


def _parse_board_field(field: str) -> list[Piece | None]:
    ranks = field.split("/")
    if len(ranks) != 8:
        raise FenError(f"Board field must have exactly 8 ranks: {field!r}")

    board: list[Piece | None] = [None] * 64

    for fen_rank_index, rank_text in enumerate(ranks):
        board_rank = 7 - fen_rank_index
        file_index = 0

        for char in rank_text:
            if char.isdigit():
                empty_count = int(char)
                if not 1 <= empty_count <= 8:
                    raise FenError(f"Invalid empty-square count in board field: {field!r}")
                file_index += empty_count
            else:
                if file_index >= 8:
                    raise FenError(f"Too many squares in rank: {rank_text!r}")
                square = rank_file_to_index(board_rank, file_index)
                board[square] = Piece.from_fen_char(char)
                file_index += 1

        if file_index != 8:
            raise FenError(f"Rank does not contain exactly 8 squares: {rank_text!r}")

    return board


def _serialize_board_field(position: Position) -> str:
    ranks: list[str] = []

    for board_rank in range(7, -1, -1):
        empty_count = 0
        parts: list[str] = []

        for file_index in range(8):
            square = rank_file_to_index(board_rank, file_index)
            piece = position.board[square]

            if piece is None:
                empty_count += 1
                continue

            if empty_count:
                parts.append(str(empty_count))
                empty_count = 0

            parts.append(piece.to_fen_char())

        if empty_count:
            parts.append(str(empty_count))

        ranks.append("".join(parts))

    return "/".join(ranks)


def _parse_side_field(field: str) -> Color:
    if field == "w":
        return Color.WHITE
    if field == "b":
        return Color.BLACK
    raise FenError(f"Invalid side-to-move field: {field!r}")


def _parse_en_passant_field(field: str) -> int | None:
    if field == "-":
        return None

    try:
        square = coord_to_index(field)
    except InvalidSquareError as exc:
        raise FenError(f"Invalid en passant field: {field!r}") from exc

    rank = field[1]
    if rank not in {"3", "6"}:
        raise FenError(f"En passant square must be on rank 3 or 6: {field!r}")

    return square


def _parse_halfmove_field(field: str) -> int:
    try:
        value = int(field)
    except ValueError as exc:
        raise FenError(f"Invalid halfmove clock: {field!r}") from exc

    if value < 0:
        raise FenError(f"Halfmove clock cannot be negative: {field!r}")
    return value


def _parse_fullmove_field(field: str) -> int:
    try:
        value = int(field)
    except ValueError as exc:
        raise FenError(f"Invalid fullmove number: {field!r}") from exc

    if value <= 0:
        raise FenError(f"Fullmove number must be positive: {field!r}")
    return value