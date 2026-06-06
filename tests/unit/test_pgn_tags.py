from chesslab.engine.game.game_record import GameRecord
from chesslab.io.pgn import export_pgn


def test_pgn_contains_required_tags() -> None:
    record = GameRecord(
        event="Test Event",
        site="Test Site",
        date="2026.06.05",
        round="1",
        white="Alice",
        black="Engine",
        result="1-0",
    )
    pgn = export_pgn(record)

    assert '[Event "Test Event"]' in pgn
    assert '[Site "Test Site"]' in pgn
    assert '[Date "2026.06.05"]' in pgn
    assert '[Round "1"]' in pgn
    assert '[White "Alice"]' in pgn
    assert '[Black "Engine"]' in pgn
    assert '[Result "1-0"]' in pgn