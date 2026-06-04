from chesslab.engine.board import (
    coord_to_index,
    index_to_coord,
    index_to_rank_file,
    rank_file_to_index,
)


def test_known_coordinates() -> None:
    assert coord_to_index("a1") == 0
    assert coord_to_index("h1") == 7
    assert coord_to_index("a8") == 56
    assert coord_to_index("h8") == 63


def test_known_inverse_coordinates() -> None:
    assert index_to_coord(0) == "a1"
    assert index_to_coord(7) == "h1"
    assert index_to_coord(56) == "a8"
    assert index_to_coord(63) == "h8"


def test_round_trip_examples() -> None:
    for coord in ("a1", "c2", "e4", "h8", "b7"):
        assert index_to_coord(coord_to_index(coord)) == coord


def test_rank_file_round_trip() -> None:
    rank = 3
    file = 4
    index = rank_file_to_index(rank, file)
    assert index_to_rank_file(index) == (rank, file)