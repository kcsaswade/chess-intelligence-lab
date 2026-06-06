from chesslab.engine.eval.result import EvaluationResult
from chesslab.engine.game.history import GameHistory, GameHistoryEntry
from chesslab.engine.move import Move
from chesslab.engine.search.stats import SearchStats


def test_game_history_appends_in_ply_order() -> None:
    history = GameHistory()
    entry1 = GameHistoryEntry(
        ply=1,
        move=Move(12, 28),
        fen_before="before1",
        fen_after="after1",
        evaluation=EvaluationResult(0, 0, 0, 0, 0, 0, 0),
        search_stats=SearchStats(1, 0, 1, 1.0, []),
    )
    entry2 = GameHistoryEntry(
        ply=2,
        move=Move(52, 36),
        fen_before="before2",
        fen_after="after2",
        evaluation=EvaluationResult(0, 0, 0, 0, 0, 0, 0),
        search_stats=SearchStats(2, 0, 1, 1.5, []),
    )

    history.append(entry1)
    history.append(entry2)

    assert len(history.entries) == 2
    assert history.entries[0].ply == 1
    assert history.entries[1].ply == 2