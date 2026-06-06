from chesslab.engine.search.config import SearchConfig
from chesslab.engine.search.engine_search import search_position
from chesslab.engine.telemetry.search_log import build_search_log_entry
from chesslab.io.fen import parse_fen
from chesslab.io.serializers import search_log_entry_to_dict


def test_logged_search_from_fen_serializes() -> None:
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

    payload = search_log_entry_to_dict(entry)
    assert payload["position_fen"]
    assert payload["engine_version"]