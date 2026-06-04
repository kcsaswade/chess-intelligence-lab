"""Minimal CLI entry point for the Chess Intelligence Laboratory."""

from __future__ import annotations

from chesslab.constants import APP_NAME, CLI_DESCRIPTION, VERSION_STRING


def build_startup_message() -> str:
    """Return the CLI startup message."""
    lines = [
        APP_NAME,
        f"Version: {VERSION_STRING}",
        CLI_DESCRIPTION,
        "",
        "Available modes (planned):",
        "  - gui",
        "  - perft",
        "  - play",
        "  - test-position",
    ]
    return "\n".join(lines)


def main() -> int:
    """Run the CLI entry point."""
    print(build_startup_message())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())