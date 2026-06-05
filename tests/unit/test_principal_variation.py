from chesslab.engine.legal_moves import is_legal_move
from chesslab.engine.make_unmake import make_move, unmake_move
from chesslab.engine.search.config import SearchConfig
from chesslab.engine.search.engine_search import search_position
from chesslab.io.fen import parse_fen


def test_principal_variation_starts_with_best_move_and_is_legal_sequence() -> None:
    position = parse_fen("4k3/8/8/3p4/4P3/8/8/4K3 w - - 0 1")
    result = search_position(position, SearchConfig(depth=3))
    pv = result.stats.principal_variation

    assert pv
    assert result.best_move == pv[0]
    assert len(pv) <= 3

    undos = []
    try:
        for move in pv:
            assert is_legal_move(position, move)
            undo = make_move(position, move)
            undos.append((move, undo))
    finally:
        for move, undo in reversed(undos):
            unmake_move(position, move, undo)