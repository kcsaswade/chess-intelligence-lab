from chesslab.engine.search.config import SearchConfig
from chesslab.engine.search.engine_search import search_position
from chesslab.engine.telemetry.search_log import build_search_log_entry
from chesslab.io.fen import parse_fen


def test_search_log_entry_contains_required_fields() -> None:
    position = parse_fen("4k3/8/8/8/8/8/8/4KQ2 w - - 0 1")
    config = SearchConfig(depth=1)
    result = search_position(position, config)

    entry = build_search_log_entry(
        game_id="game-1",
        ply=1,
        position=position,
        result=result,
        config=config,
    )

    assert entry.position_fen
    assert entry.score == result.score
    assert "material" in entry.eval_components
    assert entry.nodes >= 0
    assert entry.cutoffs >= 0
    assert entry.depth >= 0
    assert entry.time_ms >= 0.0
    assert entry.engine_version
    assert entry.timestamp