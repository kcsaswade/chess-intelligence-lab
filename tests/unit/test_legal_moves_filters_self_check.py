from chesslab.engine.board import coord_to_index
from chesslab.engine.legal_moves import generate_legal_moves
from chesslab.engine.move_generation.generator import generate_pseudolegal_moves
from chesslab.io.fen import parse_fen


def test_self_check_moves_are_filtered_out() -> None:
    position = parse_fen("4r3/8/8/8/8/8/4R3/4K3 w - - 0 1")

    pseudo_moves = generate_pseudolegal_moves(position)
    legal_moves = generate_legal_moves(position)

    pseudo_destinations = {move.to_sq for move in pseudo_moves if 
                           move.from_sq == coord_to_index("e2")}
    legal_destinations = {move.to_sq for move in legal_moves if 
                          move.from_sq == coord_to_index("e2")}

    assert coord_to_index("f2") in pseudo_destinations
    assert coord_to_index("f2") not in legal_destinations