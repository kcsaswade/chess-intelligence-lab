from chesslab.engine.eval.weights import EvaluationWeights
from chesslab.engine.search.config import SearchConfig


def test_search_config_defaults() -> None:
    config = SearchConfig()
    assert config.depth == 3
    assert config.use_alpha_beta is True
    assert config.evaluation_weights is None


def test_search_config_overrides() -> None:
    weights = EvaluationWeights(material=120)
    config = SearchConfig(depth=2, use_alpha_beta=False, evaluation_weights=weights)
    assert config.depth == 2
    assert config.use_alpha_beta is False
    assert config.evaluation_weights == weights