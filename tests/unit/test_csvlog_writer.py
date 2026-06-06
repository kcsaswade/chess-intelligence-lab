from pathlib import Path

from chesslab.io.csvlog import write_csv_rows


def test_csv_writer_writes_header_and_rows(tmp_path: Path) -> None:
    path = tmp_path / "test.csv"
    rows = [
        {"name": "a", "value": 1},
        {"name": "b", "value": 2},
    ]

    write_csv_rows(path, rows)

    text = path.read_text(encoding="utf-8")
    assert "name,value" in text
    assert "a,1" in text
    assert "b,2" in text