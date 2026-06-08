"""Shared signal-bearing helpers for GUI coordination."""


from __future__ import annotations

from PySide6.QtCore import QObject, Signal


class GuiSignals(QObject):
    """Optional shared signal container."""

    move_requested = Signal(object)
    search_finished = Signal(object)
    search_failed = Signal(str)