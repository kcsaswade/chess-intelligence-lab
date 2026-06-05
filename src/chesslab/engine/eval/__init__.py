"""Evaluation package exports."""


from chesslab.engine.eval.evaluator import evaluate, evaluate_position
from chesslab.engine.eval.result import EvaluationResult
from chesslab.engine.eval.weights import EvaluationWeights

__all__ = [
    "EvaluationResult",
    "EvaluationWeights",
    "evaluate",
    "evaluate_position",
]