import pytest
from typing import List

from testing_utils import (
    mute_logs,
    next_alphanumeric,
)
from testing_automation_common import (
    mock_parse_argv,
)
from bluetooth import Bluetooth


MODULE_NAME: str = 'bluetooth'


@pytest.mark.parametrize('argv, on', [
    ([next_alphanumeric(10)], False),
    (['off'], False),
    (['on'], True),
])
def should_have_executed(monkeypatch, argv: List[str], on: bool) -> None:
    def mock_execute_cmd(*args: tuple, **kwargs: dict) -> str:
        assert args[0] == ['blueutil', '-p', ('1' if on else '0')]
        return '\n'
    mock_parse_argv(MODULE_NAME, 'Bluetooth', monkeypatch, argv)
    monkeypatch.setattr(f"{MODULE_NAME}.execute_cmd", mock_execute_cmd)
    mute_logs(MODULE_NAME, monkeypatch)
    result: str = Bluetooth().execute()
    assert result == ''


@pytest.mark.parametrize('argv', [
    ([next_alphanumeric(10)]),
    ([]),
])
def should_not_have_parsed_argv_with_wrong_or_no_option(monkeypatch, argv: List[str]) -> None:
    def mock_raise_error(*args: tuple, **kwargs: dict) -> None:
        assert kwargs['usage'] is not None
        raise SystemExit(0)  # Controlled early exit
    monkeypatch.setattr(f"{MODULE_NAME}.raise_error", mock_raise_error)
    with pytest.raises(SystemExit) as e:
        Bluetooth(argv)
    assert e.type == SystemExit
    assert e.value.code == 0


@pytest.mark.parametrize('argv', [
    (['on']),
    (['off']),
])
def should_have_parsed_argv(argv) -> None:
    bluetooth: Bluetooth = Bluetooth(argv)
    assert bluetooth.argv == argv


def should_have_printed_usage_instructions(monkeypatch) -> None:
    print_coloured_calls: list = []
    mock_parse_argv(MODULE_NAME, 'Bluetooth', monkeypatch)
    monkeypatch.setattr(f"{MODULE_NAME}.print_coloured", lambda *a, **k: print_coloured_calls.append(''))
    Bluetooth().usage()
    assert len(print_coloured_calls) == 2
