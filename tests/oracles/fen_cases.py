"""Curated FEN cases for oracle comparisons."""


from __future__ import annotations

STARTPOS_CASES: list[dict[str, str]] = [
    {
        "name": "startpos",
        "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    },
]

LEGAL_MOVE_CASES: list[dict[str, str]] = [
    {
        "name": "simple_development",
        "fen": "rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1",
    },
    {
        "name": "pinned_piece",
        "fen": "4k3/8/8/8/8/4q3/4R3/4K3 w - - 0 1",
    },
    {
        "name": "in_check",
        "fen": "4k3/8/8/8/8/8/4q3/4K3 w - - 0 1",
    },
]

CASTLING_CASES: list[dict[str, str]] = [
    {
        "name": "white_both_castles_available",
        "fen": "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1",
    },
    {
        "name": "castling_blocked",
        "fen": "r3k2r/8/8/8/8/8/8/R2QK2R w KQkq - 0 1",
    },
    {
        "name": "castling_through_check",
        "fen": "r3k2r/8/8/8/2b5/8/8/R3K2R w KQkq - 0 1",
    },
]

EN_PASSANT_CASES: list[dict[str, str]] = [
    {
        "name": "en_passant_available",
        "fen": "4k3/8/8/3pP3/8/8/8/4K3 w - d6 0 1",
    },
    {
        "name": "en_passant_expired",
        "fen": "4k3/8/8/3pP3/8/8/8/4K3 w - - 0 1",
    },
    {
        "name": "en_passant_illegal_due_to_exposure",
        "fen": "4r1k1/8/8/3pP3/8/8/8/4K3 w - d6 0 1",
    },
]

PROMOTION_CASES: list[dict[str, str]] = [
    {
        "name": "promotion_push_all_choices",
        "fen": "4k3/6P1/8/8/8/8/8/4K3 w - - 0 1",
    },
    {
        "name": "promotion_capture_all_choices",
        "fen": "1r2k3/P7/8/8/8/8/8/4K3 w - - 0 1",
    },
]

STATUS_CASES: list[dict[str, str]] = [
    {
        "name": "checkmate",
        "fen": "7k/6Q1/6K1/8/8/8/8/8 b - - 0 1",
    },
    {
        "name": "stalemate",
        "fen": "7k/5Q2/6K1/8/8/8/8/8 b - - 0 1",
    },
]