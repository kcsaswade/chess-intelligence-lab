from chesslab.engine.eval.result import EvaluationResult
from chesslab.engine.game.game_record import GameRecord
from chesslab.engine.game.history import GameHistoryEntry
from chesslab.engine.move import Move
from chesslab.engine.search.stats import SearchStats
from chesslab.engine.telemetry.game_log import build_game_log_entry
from chesslab.io.serializers import game_log_entry_to_dict


def test_game_log_export_builds_summary() -> None:
    record = GameRecord(game_id="game-1", result="1-0")
    record.history.append(
        GameHistoryEntry(
            ply=1,
            move=Move(12, 28),
            fen_before="before",
            fen_after="after",
            evaluation=EvaluationResult(10, 1, 2, 3, 4, 0, 0),
            search_stats=SearchStats(100, 10, 2, 5.0, []),
            san="e4",
        )
    )

    entry = build_game_log_entry(record)
    payload = game_log_entry_to_dict(entry)

    assert payload["result"] == "1-0"
    assert payload["total_plies"] == 1
    assert payload["total_nodes"] == 100