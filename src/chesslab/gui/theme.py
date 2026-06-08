"""Theme helpers for the ChessLab desktop GUI."""


from __future__ import annotations

from chesslab.constants import (
    GUI_APP_BACKGROUND,
    GUI_PANEL_BACKGROUND,
    GUI_PANEL_MUTED_TEXT,
    GUI_PANEL_SURFACE,
    GUI_PANEL_TEXT,
)


def build_application_stylesheet() -> str:
    return f"""
    QMainWindow {{
        background-color: {GUI_APP_BACKGROUND};
    }}
    QWidget {{
        color: {GUI_PANEL_TEXT};
        font-size: 14px;
    }}
    QFrame#SidePanelFrame {{
        background-color: {GUI_PANEL_BACKGROUND};
        border-radius: 10px;
    }}
    QFrame#PanelCard {{
        background-color: {GUI_PANEL_SURFACE};
        border-radius: 8px;
        padding: 8px;
    }}
    QLabel#SectionTitle {{
        font-size: 16px;
        font-weight: 700;
        color: {GUI_PANEL_TEXT};
    }}
    QLabel#MutedLabel {{
        color: {GUI_PANEL_MUTED_TEXT};
    }}
    QListWidget {{
        background-color: {GUI_PANEL_SURFACE};
        border: none;
        border-radius: 8px;
        padding: 6px;
    }}
    QTableWidget {{
        background-color: {GUI_PANEL_SURFACE};
        border: none;
        border-radius: 8px;
        gridline-color: transparent;
    }}
    QHeaderView::section {{
        background-color: {GUI_PANEL_SURFACE};
        border: none;
        padding: 4px;
        font-weight: 700;
    }}
    QPushButton {{
        background-color: {GUI_PANEL_SURFACE};
        border-radius: 6px;
        padding: 8px 12px;
    }}
    QPushButton:hover {{
        background-color: #363C46;
    }}
    """