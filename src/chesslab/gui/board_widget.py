"""Interactive chessboard widget."""


from __future__ import annotations


from PySide6.QtCore import QPoint, QRect, Qt, Signal
from PySide6.QtGui import QColor, QMouseEvent, QPainter, QPen, QPaintEvent
from PySide6.QtWidgets import QSizePolicy, QWidget

from chesslab.constants import (
    GUI_DARK_SQUARE,
    GUI_LAST_MOVE_HIGHLIGHT,
    GUI_LEGAL_MOVE_HINT,
    GUI_LIGHT_SQUARE,
    GUI_MIN_BOARD_SIZE,
    GUI_SELECTED_SQUARE,
)
from chesslab.engine.legal_moves import generate_legal_moves
from chesslab.engine.move import Move
from chesslab.engine.position import Position
from chesslab.gui.resources import load_piece_pixmap


class BoardWidget(QWidget):
    """Painted board widget with click-click move input."""

    move_requested = Signal(object)
    square_selected = Signal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._position: Position | None = None
        self._selected_square: int | None = None
        self._legal_targets: dict[int, bool] = {}
        self._enabled_for_human = True
        self._last_move: Move | None = None

        self.setMinimumSize(GUI_MIN_BOARD_SIZE, GUI_MIN_BOARD_SIZE)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def set_position(self, position: Position, *, last_move: Move | None = None) -> None:
        self._position = position
        self._last_move = last_move
        self.clear_selection()
        self.update()

    def set_enabled_for_human(self, enabled: bool) -> None:
        self._enabled_for_human = enabled
        if not enabled:
            self.clear_selection()
        self.update()

    def clear_selection(self) -> None:
        self._selected_square = None
        self._legal_targets = {}
        self.update()

    def square_rect(self, square: int) -> QRect:
        board_rect = self._board_rect()
        square_size = board_rect.width() // 8
        file_index = square % 8
        rank_index = square // 8
        draw_rank = 7 - rank_index
        x = board_rect.left() + (file_index * square_size)
        y = board_rect.top() + (draw_rank * square_size)
        return QRect(x, y, square_size, square_size)

    def square_at(self, point: QPoint) -> int | None:
        board_rect = self._board_rect()
        if not board_rect.contains(point):
            return None
        square_size = board_rect.width() // 8
        file_index = (point.x() - board_rect.left()) // square_size
        draw_rank = (point.y() - board_rect.top()) // square_size
        rank_index = 7 - draw_rank
        return int(rank_index * 8 + file_index)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if not self._enabled_for_human or self._position is None:
            return
        if event.button() != Qt.MouseButton.LeftButton:
            return

        square = self.square_at(event.position().toPoint())
        if square is None:
            self.clear_selection()
            return

        position = self._position
        piece = position.piece_at(square)

        if self._selected_square is None:
            if piece is None or piece.color is not position.side_to_move:
                return
            self._select_square(square)
            return

        if square == self._selected_square:
            self.clear_selection()
            return

        if square in self._legal_targets:
            legal_move = self._resolve_move(self._selected_square, square)
            if legal_move is not None:
                self.move_requested.emit(legal_move)
                self.clear_selection()
                return

        if piece is not None and piece.color is position.side_to_move:
            self._select_square(square)
            return

        self.clear_selection()

    def _select_square(self, square: int) -> None:
        position = self._position
        if position is None:
            return

        targets: dict[int, bool] = {}
        for move in generate_legal_moves(position):
            if move.from_sq != square:
                continue
            is_capture = position.piece_at(move.to_sq) is not None or move.is_capture or move.is_en_passant
            targets[move.to_sq] = is_capture

        self._selected_square = square
        self._legal_targets = targets
        self.square_selected.emit(square)
        self.update()

    def _resolve_move(self, from_sq: int, to_sq: int) -> Move | None:
        position = self._position
        if position is None:
            return None
        matching = [
            move for move in generate_legal_moves(position)
            if move.from_sq == from_sq and move.to_sq == to_sq
        ]
        if not matching:
            return None
        non_promotion = [move for move in matching if move.promotion is None]
        if non_promotion:
            return non_promotion[0]
        return matching[0]

    def paintEvent(self, event: QPaintEvent) -> None:
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        for square in range(64):
            rect = self.square_rect(square)
            color = self._square_color(square)
            painter.fillRect(rect, color)

            if self._last_move is not None and square in {self._last_move.from_sq, self._last_move.to_sq}:
                painter.fillRect(rect, QColor(GUI_LAST_MOVE_HIGHLIGHT))

            if self._selected_square == square:
                painter.fillRect(rect, QColor(GUI_SELECTED_SQUARE))

        for square, is_capture in self._legal_targets.items():
            rect = self.square_rect(square)
            center = rect.center()
            hint_color = QColor(GUI_LEGAL_MOVE_HINT)

            if is_capture:
                pen = QPen(hint_color)
                pen.setWidth(max(3, rect.width() // 14))
                painter.setPen(pen)
                painter.setBrush(Qt.BrushStyle.NoBrush)
                inset = max(6, rect.width() // 10)
                painter.drawEllipse(rect.adjusted(inset, inset, -inset, -inset))
            else:
                painter.setPen(Qt.PenStyle.NoPen)
                dot_color = QColor(hint_color)
                dot_color.setAlpha(180)
                painter.setBrush(dot_color)
                radius = max(6, rect.width() // 8)
                painter.drawEllipse(center, radius, radius)

        position = self._position
        if position is not None:
            square_size = self.square_rect(0).width()
            piece_size = max(24, square_size - 10)
            for square, piece in enumerate(position.board):
                if piece is None:
                    continue
                rect = self.square_rect(square)
                pixmap = load_piece_pixmap(piece, piece_size)
                x = rect.left() + (rect.width() - piece_size) // 2
                y = rect.top() + (rect.height() - piece_size) // 2
                painter.drawPixmap(x, y, pixmap)

        border_pen = QPen(QColor("#111111"))
        border_pen.setWidth(2)
        painter.setPen(border_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(self._board_rect())

    def _square_color(self, square: int) -> QColor:
        rank_index = square // 8
        file_index = square % 8
        return QColor(GUI_LIGHT_SQUARE if (rank_index + file_index) % 2 == 0 else GUI_DARK_SQUARE)

    def _board_rect(self) -> QRect:
        board_size = min(self.width(), self.height())
        board_size -= board_size % 8
        left = (self.width() - board_size) // 2
        top = (self.height() - board_size) // 2
        return QRect(left, top, board_size, board_size)