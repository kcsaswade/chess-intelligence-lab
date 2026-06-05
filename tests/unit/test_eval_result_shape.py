from chesslab.engine.eval.evaluator import evaluate
from chesslab.io.fen import parse_fen


def test_evaluation_result_has_full_component_shape() -> None:
    position = parse_fen("4k3/8/8/8/8/8/8/4K3 w - - 0 1")
    result = evaluate(position)

    assert hasattr(result, "total")
    assert hasattr(result, "material")
    assert hasattr(result, "mobility")
    assert hasattr(result, "king_safety")
    assert hasattr(result, "pawn_structure")
    assert hasattr(result, "center_control")
    assert hasattr(result, "piece_activity")

    assert result.total == (
        result.material
        + result.mobility
        + result.king_safety
        + result.pawn_structure
        + result.center_control
        + result.piece_activity
    )