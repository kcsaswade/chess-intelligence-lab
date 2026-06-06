"""Minimal SAN conversion for legal moves."""


from __future__ import annotations

from chesslab.engine.game_status import is_checkmate
from chesslab.engine.legal_moves import generate_legal_moves
from chesslab.engine.make_unmake import make_move, unmake_move
from chesslab.engine.move import Move
from chesslab.engine.piece import PieceType
from chesslab.engine.position import Position

_PIECE_LETTERS = {
    PieceType.KING: "K",
    PieceType.QUEEN: "Q",
    PieceType.ROOK: "R",
    PieceType.BISHOP: "B",
    PieceType.KNIGHT: "N",
}


def _square_name(square: int) -> str:
    file_index = square % 8
    rank_index = square // 8
    return f"{'abcdefgh'[file_index]}{'12345678'[rank_index]}"


def _promotion_suffix(move: Move) -> str:
    if move.promotion is None:
        return ""
    return f"={_PIECE_LETTERS[move.promotion]}"


def _is_capture(position: Position, move: Move) -> bool:
    return move.is_capture or move.is_en_passant or position.piece_at(move.to_sq) is not None


def _disambiguation(position: Position, move: Move) -> str:
    moving_piece = position.piece_at(move.from_sq)
    if moving_piece is None or moving_piece.kind is PieceType.PAWN:
        return ""

    candidates: list[Move] = []
    for legal_move in generate_legal_moves(position):
        if legal_move == move:
            continue
        other_piece = position.piece_at(legal_move.from_sq)
        if (
            legal_move.to_sq == move.to_sq
            and other_piece is not None
            and other_piece.color is moving_piece.color
            and other_piece.kind is moving_piece.kind
        ):
            candidates.append(legal_move)

    if not candidates:
        return ""

    from_file = move.from_sq % 8
    from_rank = move.from_sq // 8

    same_file = any(candidate.from_sq % 8 == from_file for candidate in candidates)
    same_rank = any(candidate.from_sq // 8 == from_rank for candidate in candidates)

    if not same_file:
        return "abcdefgh"[from_file]
    if not same_rank:
        return "12345678"[from_rank]
    return f"{'abcdefgh'[from_file]}{'12345678'[from_rank]}"


def move_to_san(position: Position, move: Move) -> str:
    piece = position.piece_at(move.from_sq)
    if piece is None:
        raise ValueError("No piece found at SAN source square")

    if move.is_castling:
        san = "O-O" if move.to_sq > move.from_sq else "O-O-O"
    elif piece.kind is PieceType.PAWN:
        capture_marker = "x" if _is_capture(position, move) else ""
        origin_file = "abcdefgh"[move.from_sq % 8]
        destination = _square_name(move.to_sq)
        if capture_marker:
            san = f"{origin_file}{capture_marker}{destination}{_promotion_suffix(move)}"
        else:
            san = f"{destination}{_promotion_suffix(move)}"
    else:
        piece_letter = _PIECE_LETTERS[piece.kind]
        capture_marker = "x" if _is_capture(position, move) else ""
        destination = _square_name(move.to_sq)
        san = f"{piece_letter}{_disambiguation(position, move)}{capture_marker}{destination}{_promotion_suffix(move)}"

    undo = make_move(position, move)
    try:
        enemy_moves = generate_legal_moves(position)
        if not enemy_moves and is_checkmate(position):
            san += "#"
        else:
            from chesslab.engine.attacks import is_in_check
            if is_in_check(position, position.side_to_move):
                san += "+"
    finally:
        unmake_move(position, move, undo)

    return san