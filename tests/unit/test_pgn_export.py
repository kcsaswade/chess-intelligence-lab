from chesslab.engine.eval.result import EvaluationResult
from chesslab.engine.game.game_record import GameRecord
from chesslab.engine.game.history import GameHistoryEntry
from chesslab.engine.move import Move
from chesslab.engine.search.stats import SearchStats
from chesslab.io.pgn import export_pgn


def test_pgn_export_contains_movetext_and_result() -> None:
    record = GameRecord(
        event="Test Event",
        site="Test Site",
        date="2026.06.05",
        round="1",
        white="Alice",
        black="Engine",
        result="1-0",
    )
    record.history.append(
        GameHistoryEntry(
            ply=1,
            move=Move(12, 28),
            fen_before="before",
            fen_after="after",
            evaluation=EvaluationResult(0, 0, 0, 0, 0, 0, 0),
            search_stats=SearchStats(0, 0, 0, 0.0, []),
            san="e4",
        )
    )

    pgn = export_pgn(record)
    assert "1. e4 1-0" in pgn