import json
from pathlib import Path

from chesslab.io.jsonlog import append_jsonl_entry


def test_jsonl_writer_appends_one_json_object_per_line(tmp_path: Path) -> None:
    path = tmp_path / "test.jsonl"

    append_jsonl_entry(path, {"a": 1})
    append_jsonl_entry(path, {"b": 2})

    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0]) == {"a": 1}
    assert json.loads(lines[1]) == {"b": 2}