from chesslab.constants import VERSION_STRING
from chesslab.engine.search.config import SearchConfig
from chesslab.engine.search.engine_search import search_position
from chesslab.engine.telemetry.search_log import build_search_log_entry
from chesslab.io.fen import parse_fen


def test_engine_version_appears_in_logs() -> None:
    position = parse_fen("4k3/8/8/8/8/8/8/4KQ2 w - - 0 1")
    config = SearchConfig(depth=1)
    result = search_position(position, config)
    entry = build_search_log_entry(
        game_id="g1",
        ply=1,
        position=position,
        result=result,
        config=config,
    )
    assert entry.engine_version == VERSION_STRING