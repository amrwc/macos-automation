from typing import List

from wifi import (
    usage,
)


def should_have_printed_usage_instructions(monkeypatch) -> None:
    print_coloured_calls: List[str] = []
    monkeypatch.setattr('wifi.print_coloured', lambda *a, **k: print_coloured_calls.append(''))
    usage()
    assert len(print_coloured_calls) == 2
