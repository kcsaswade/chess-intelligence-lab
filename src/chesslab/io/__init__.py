"""IO boundary utilities for notation and serialization."""

from chesslab.io.csvlog import append_csv_row, write_csv_rows
from chesslab.io.fen import parse_fen, to_fen
from chesslab.io.jsonlog import append_jsonl_entry, write_jsonl_entries
from chesslab.io.pgn import export_pgn
from chesslab.io.san import move_to_san
from chesslab.io.serializers import (
    evaluation_result_to_dict,
    game_log_entry_to_dict,
    search_config_to_dict,
    search_log_entry_to_dict,
    search_stats_to_dict,
)

__all__ = [
    "append_csv_row",
    "append_jsonl_entry",
    "evaluation_result_to_dict",
    "export_pgn",
    "game_log_entry_to_dict",
    "move_to_san",
    "parse_fen",
    "search_config_to_dict",
    "search_log_entry_to_dict",
    "search_stats_to_dict",
    "to_fen",
    "write_csv_rows",
    "write_jsonl_entries",
]