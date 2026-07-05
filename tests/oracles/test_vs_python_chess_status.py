"""Oracle tests for status outcomes."""


from __future__ import annotations

from tests.oracles.fen_cases import STATUS_CASES
from tests.oracles.state_compare import assert_status_matches


def test_status_positions_match_python_chess() -> None:
    for case in STATUS_CASES:
        assert_status_matches(case["fen"])