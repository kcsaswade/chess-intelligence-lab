from chesslab.constants import DRAW_SCORE, MATE_SCORE
from chesslab.engine.search.config import SearchConfig
from chesslab.engine.search.engine_search import search_position
from chesslab.io.fen import parse_fen


def test_checkmate_position_returns_extreme_score() -> None:
    position = parse_fen("7k/6Q1/6K1/8/8/8/8/8 b - - 0 1")
    result = search_position(position, SearchConfig(depth=2))
    assert result.best_move is None
    assert result.score <= -MATE_SCORE + 1


def test_stalemate_returns_draw_score() -> None:
    position = parse_fen("7k/5Q2/6K1/8/8/8/8/8 b - - 0 1")
    result = search_position(position, SearchConfig(depth=2))
    assert result.best_move is None
    assert result.score == DRAW_SCORE