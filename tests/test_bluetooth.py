from typing import List

import pytest

from bluetooth import Bluetooth
from .testing_automation_common import mock_parse_argv
from .testing_utils import mute_logs, next_alphanumeric

MODULE_NAME = 'bluetooth'


def should_have_raised_exception_when_blueutils_is_not_installed(monkeypatch) -> None:
    def mock_execute_cmd(*args: tuple, **kwargs: dict) -> None:
        exception = Exception()
        exception.message = "No such file or directory: 'blueutil'"
        raise exception

    def mock_raise_error(*args: tuple, **kwargs: dict) -> None:
        assert 'blueutil' in args[0]
        raise SystemExit(0)  # Controlled early exit

    mock_parse_argv(MODULE_NAME, 'Bluetooth', monkeypatch, ['on'])
    monkeypatch.setattr(f"{MODULE_NAME}.execute_cmd", mock_execute_cmd)
    monkeypatch.setattr(f"{MODULE_NAME}.raise_error", mock_raise_error)
    mute_logs(MODULE_NAME, monkeypatch)
    with pytest.raises(SystemExit) as e:
        Bluetooth().execute()
    assert e.type == SystemExit
    assert e.value.code == 0


def should_have_returned_unhandled_error(monkeypatch) -> None:
    error_message = next_alphanumeric(16)

    def mock_execute_cmd(*args: tuple, **kwargs: dict) -> None:
        exception = Exception()
        exception.message = error_message
        raise exception

    mock_parse_argv(MODULE_NAME, 'Bluetooth', monkeypatch, ['on'])
    monkeypatch.setattr(f"{MODULE_NAME}.execute_cmd", mock_execute_cmd)
    mute_logs(MODULE_NAME, monkeypatch)
    assert error_message in Bluetooth().execute()


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
    assert Bluetooth().execute() == ''


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
def should_have_parsed_argv(argv: List[str]) -> None:
    assert Bluetooth(argv).argv == argv


def should_have_printed_usage_instructions(monkeypatch) -> None:
    print_coloured_calls = []
    mock_parse_argv(MODULE_NAME, 'Bluetooth', monkeypatch)
    monkeypatch.setattr(f"{MODULE_NAME}.print_coloured", lambda *a, **k: print_coloured_calls.append(''))
    Bluetooth().usage()
    assert len(print_coloured_calls) == 2
