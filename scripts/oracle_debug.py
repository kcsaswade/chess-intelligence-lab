"""Quick oracle diff tool for a single FEN."""


from __future__ import annotations

import sys

from tests.oracles.adapters import our_legal_moves_uci, python_chess_legal_moves_uci


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/oracle_debug.py '<fen>'")
        return 1

    fen = sys.argv[1]
    ours = our_legal_moves_uci(fen)
    oracle = python_chess_legal_moves_uci(fen)

    print("Only ours:")
    for move in sorted(ours - oracle):
        print(move)

    print("\nOnly python-chess:")
    for move in sorted(oracle - ours):
        print(move)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())