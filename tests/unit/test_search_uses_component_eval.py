from chesslab.engine.search.config import SearchConfig
from chesslab.engine.search.engine_search import search_position
from chesslab.io.fen import parse_fen


def test_search_result_exposes_component_evaluation() -> None:
    position = parse_fen("r1bqkbnr/pppp1ppp/2n5/4p3/3P4/5N2/PPP1PPPP/RNBQKB1R b KQkq - 1 3")
    result = search_position(position, SearchConfig(depth=2))

    assert result.evaluation.total == (
        result.evaluation.material
        + result.evaluation.mobility
        + result.evaluation.king_safety
        + result.evaluation.pawn_structure
        + result.evaluation.center_control
        + result.evaluation.piece_activity
    )