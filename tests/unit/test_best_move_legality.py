from chesslab.engine.legal_moves import generate_legal_moves
from chesslab.engine.search.config import SearchConfig
from chesslab.engine.search.engine_search import search_position
from chesslab.io.fen import parse_fen


def test_best_move_is_legal() -> None:
    position = parse_fen("r1bqkbnr/pppp1ppp/2n5/4p3/3P4/5N2/PPP1PPPP/RNBQKB1R b KQkq - 1 3")
    result = search_position(position, SearchConfig(depth=2))
    legal_moves = generate_legal_moves(position)
    assert result.best_move in legal_moves