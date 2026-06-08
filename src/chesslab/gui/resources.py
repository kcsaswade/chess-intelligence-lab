"""GUI resource loading helpers."""


from __future__ import annotations

from pathlib import Path

from PySide6.QtGui import QColor, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

from chesslab.engine.piece import Color, Piece, PieceType

_ASSET_DIR = Path(__file__).resolve().parent / "assets" / "pieces"

_PIECE_FILE_MAP = {
    (Color.WHITE, PieceType.PAWN): "wP.svg",
    (Color.WHITE, PieceType.KNIGHT): "wN.svg",
    (Color.WHITE, PieceType.BISHOP): "wB.svg",
    (Color.WHITE, PieceType.ROOK): "wR.svg",
    (Color.WHITE, PieceType.QUEEN): "wQ.svg",
    (Color.WHITE, PieceType.KING): "wK.svg",
    (Color.BLACK, PieceType.PAWN): "bP.svg",
    (Color.BLACK, PieceType.KNIGHT): "bN.svg",
    (Color.BLACK, PieceType.BISHOP): "bB.svg",
    (Color.BLACK, PieceType.ROOK): "bR.svg",
    (Color.BLACK, PieceType.QUEEN): "bQ.svg",
    (Color.BLACK, PieceType.KING): "bK.svg",
}


def piece_asset_path(piece: Piece) -> Path:
    return _ASSET_DIR / _PIECE_FILE_MAP[(piece.color, piece.kind)]


def load_piece_pixmap(piece: Piece, size: int) -> QPixmap:
    path = piece_asset_path(piece)
    renderer = QSvgRenderer(str(path))
    pixmap = QPixmap(size, size)
    pixmap.fill(QColor(0, 0, 0, 0))
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return pixmap


def board_coordinates(square: int) -> tuple[int, int]:
    file_index = square % 8
    rank_index = square // 8
    return rank_index, file_index


def square_name(square: int) -> str:
    files = "abcdefgh"
    ranks = "12345678"
    return f"{files[square % 8]}{ranks[square // 8]}"