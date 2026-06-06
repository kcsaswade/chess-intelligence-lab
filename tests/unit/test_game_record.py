from chesslab.engine.game.game_record import GameRecord


def test_game_record_preserves_metadata() -> None:
    record = GameRecord(
        event="Event",
        site="Site",
        date="2026.06.05",
        round="2",
        white="Human",
        black="Engine",
        result="1/2-1/2",
        game_id="g-1",
    )

    assert record.event == "Event"
    assert record.site == "Site"
    assert record.result == "1/2-1/2"
    assert record.game_id == "g-1"