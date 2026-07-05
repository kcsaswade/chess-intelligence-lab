"""Adapters between ChessLab and python-chess for oracle tests."""


from __future__ import annotations

from collections.abc import Iterable

import chess

from chesslab.engine.game_status import is_checkmate, is_draw, is_stalemate
from chesslab.engine.legal_moves import generate_legal_moves
from chesslab.engine.make_unmake import make_move, unmake_move
from chesslab.engine.move import Move
from chesslab.engine.piece import PieceType
from chesslab.engine.position import Position
from chesslab.io.fen import parse_fen, to_fen
from chesslab.io.san import move_to_san

_PROMOTION_MAP: dict[str, PieceType] = {
    "q": PieceType.QUEEN,
    "r": PieceType.ROOK,
    "b": PieceType.BISHOP,
    "n": PieceType.KNIGHT,
}


def to_python_chess_board(fen: str) -> chess.Board:
    return chess.Board(fen)


def to_our_position(fen: str) -> Position:
    return parse_fen(fen)


def square_name(square: int) -> str:
    files = "abcdefgh"
    ranks = "12345678"
    return f"{files[square % 8]}{ranks[square // 8]}"

def python_chess_strict_fen(fen: str) -> str:
    board = to_python_chess_board(fen)
    return board.fen(en_passant="fen")

def move_to_uci(move: Move) -> str:
    text = f"{square_name(move.from_sq)}{square_name(move.to_sq)}"
    if move.promotion is not None:
        text += move.promotion.value
    return text


def uci_to_our_move(position: Position, uci: str) -> Move:
    legal_moves = generate_legal_moves(position)
    for move in legal_moves:
        if move_to_uci(move) == uci:
            return move
    raise ValueError(f"Move {uci!r} is not legal in our engine for FEN: {to_fen(position)}")


def our_legal_moves_uci(fen: str) -> set[str]:
    position = to_our_position(fen)
    return {move_to_uci(move) for move in generate_legal_moves(position)}


def python_chess_legal_moves_uci(fen: str) -> set[str]:
    board = to_python_chess_board(fen)
    return {move.uci() for move in board.legal_moves}


def apply_our_move_and_get_fen(fen: str, uci: str) -> str:
    position = to_our_position(fen)
    move = uci_to_our_move(position, uci)
    make_move(position, move)
    return to_fen(position)


def apply_python_chess_move_and_get_fen(fen: str, uci: str) -> str:
    board = to_python_chess_board(fen)
    move = chess.Move.from_uci(uci)
    if move not in board.legal_moves:
        raise ValueError(f"Move {uci!r} is not legal in python-chess for FEN: {fen}")
    board.push(move)
    return board.fen(en_passant="fen")


def make_unmake_our_move_returns_to_same_fen(fen: str, uci: str) -> bool:
    position = to_our_position(fen)
    original_fen = to_fen(position)
    move = uci_to_our_move(position, uci)
    undo = make_move(position, move)
    unmake_move(position, move, undo)
    return to_fen(position) == original_fen


def our_status(fen: str) -> dict[str, bool]:
    position = to_our_position(fen)
    return {
        "is_checkmate": is_checkmate(position),
        "is_stalemate": is_stalemate(position),
        "is_draw": is_draw(position),
    }


def python_chess_status(fen: str) -> dict[str, bool]:
    board = to_python_chess_board(fen)
    return {
        "is_checkmate": board.is_checkmate(),
        "is_stalemate": board.is_stalemate(),
        "is_draw": board.is_stalemate() or board.is_insufficient_material() or board.can_claim_fifty_moves() or board.is_fifty_moves(),
    }


def our_san_for_move(fen: str, uci: str) -> str:
    position = to_our_position(fen)
    move = uci_to_our_move(position, uci)
    return move_to_san(position, move)


def python_chess_san_for_move(fen: str, uci: str) -> str:
    board = to_python_chess_board(fen)
    move = chess.Move.from_uci(uci)
    if move not in board.legal_moves:
        raise ValueError(f"Move {uci!r} is not legal in python-chess for FEN: {fen}")
    return board.san(move)


def python_chess_play_line_to_pgn(start_fen: str, uci_moves: Iterable[str]) -> tuple[str, list[str], str]:
    import chess.pgn

    board = chess.Board(start_fen)
    game = chess.pgn.Game()
    if start_fen != chess.STARTING_FEN:
        game.setup(board.copy(stack=False))
        game.headers["FEN"] = start_fen
        game.headers["SetUp"] = "1"

    node = game
    san_moves: list[str] = []
    for uci in uci_moves:
        move = chess.Move.from_uci(uci)
        san_moves.append(board.san(move))
        board.push(move)
        node = node.add_variation(move)

    game.headers["Result"] = board.result(claim_draw=True) if board.is_game_over(claim_draw=True) else "*"
    exporter = chess.pgn.StringExporter(headers=True, variations=False, comments=False)
    return str(game.accept(exporter)), san_moves, game.headers["Result"]


def normalize_pgn_whitespace(text: str) -> str:
    return " ".join(text.split())