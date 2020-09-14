from typing import List


def mock_parse_argv(module_name, class_name, monkeypatch, argv: List[str] = None) -> None:
    monkeypatch.setattr(f"{module_name}.{class_name}.parse_argv", lambda *a, **k: argv)
