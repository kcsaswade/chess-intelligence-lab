"""Shared pytest fixtures and helpers."""


from __future__ import annotations

import json
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).resolve().parent
DATA_DIR = TESTS_DIR.parent / "data" / "oracle_positions"


def load_oracle_json(filename: str) -> list[dict[str, object]]:
    path = DATA_DIR / filename
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"Expected list in oracle file: {filename}")
    return data


@pytest.fixture
def oracle_data_dir() -> Path:
    return DATA_DIR


@pytest.fixture
def legal_move_cases() -> list[dict[str, object]]:
    return load_oracle_json("legal_move_cases.json")


@pytest.fixture
def castling_cases() -> list[dict[str, object]]:
    return load_oracle_json("castling_cases.json")


@pytest.fixture
def en_passant_cases() -> list[dict[str, object]]:
    return load_oracle_json("en_passant_cases.json")


@pytest.fixture
def promotion_cases() -> list[dict[str, object]]:
    return load_oracle_json("promotion_cases.json")


@pytest.fixture
def mate_stalemate_cases() -> list[dict[str, object]]:
    return load_oracle_json("mate_stalemate_cases.json")


@pytest.fixture
def make_unmake_lines() -> list[dict[str, object]]:
    return load_oracle_json("make_unmake_lines.json")