from chesslab.engine.search.config import SearchConfig
from chesslab.engine.search.engine_search import search_position
from chesslab.io.fen import parse_fen


def test_alpha_beta_matches_plain_minimax() -> None:
    position = parse_fen("4k3/8/8/3p4/4P3/8/8/4K3 w - - 0 1")
    alpha_beta = search_position(position, SearchConfig(depth=3, use_alpha_beta=True))
    plain = search_position(position, SearchConfig(depth=3, use_alpha_beta=False))
    assert alpha_beta.best_move == plain.best_move
    assert alpha_beta.score == plain.score