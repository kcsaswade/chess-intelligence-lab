# Chess Intelligence Laboratory

A staged Python chess-engine project with a headless engine core, desktop GUI, telemetry, and experiment-ready architecture.

## Stage 1 status

Chunk 1 focuses on project structure only:
- installable `src`-layout package
- minimal CLI entry point
- minimal PySide6 GUI shell
- pytest, Ruff, and mypy configuration

No chess logic is implemented yet.

## Requirements

- Python 3.11+

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Commands

Run tests:

```bash
python -m pytest
```

Run linting:

```bash
ruff check .
```

Run type checking:

```bash
mypy src
```

Run CLI:

```bash
chesslab
```

Run GUI:

```bash
chesslab-gui
```

## Planned architecture

- `src/chesslab/engine/` — core engine and rules
- `src/chesslab/search/` — minimax, alpha-beta, PV, stats
- `src/chesslab/eval/` — evaluation components and weights
- `src/chesslab/gui/` — PySide6 desktop client
- `src/chesslab/io/` — FEN, PGN, log serialization
- `src/chesslab/telemetry/` — structured search and game logging