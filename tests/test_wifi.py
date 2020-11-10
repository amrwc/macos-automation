from typing import List

import pytest

from wifi import Wifi
from .testing_automation_common import mock_parse_argv
from .testing_utils import mute_logs, next_alphabetic, next_alphanumeric

MODULE_NAME = 'wifi'


@pytest.mark.parametrize('argv, on', [
    ([next_alphanumeric(10)], False),
    (['off'], False),
    (['on'], True),
])
def should_have_executed(monkeypatch, argv: List[str], on: bool) -> None:
    def mock_set_wifi(*args: tuple, **kwargs: dict) -> str:
        assert args[1] == on
        return ''
    mock_parse_argv(MODULE_NAME, 'Wifi', monkeypatch, argv)
    monkeypatch.setattr(f"{MODULE_NAME}.Wifi.set_wifi", mock_set_wifi)
    assert Wifi().execute() == ''


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
        Wifi(argv)
    assert e.type == SystemExit
    assert e.value.code == 0


@pytest.mark.parametrize('argv', [
    (['on']),
    (['off']),
])
def should_have_parsed_argv(argv: List[str]) -> None:
    assert Wifi(argv).argv == argv


def should_have_printed_usage_instructions(monkeypatch) -> None:
    print_coloured_calls = []
    mock_parse_argv(MODULE_NAME, 'Wifi', monkeypatch)
    monkeypatch.setattr(f"{MODULE_NAME}.print_coloured", lambda *a, **k: print_coloured_calls.append(''))
    Wifi().usage()
    assert len(print_coloured_calls) == 2


@pytest.mark.parametrize('on', [
    (True,),
    (False,),
])
def should_have_set_wifi(monkeypatch, on: bool) -> None:
    def mock_execute_cmd(*args: tuple, **kwargs: dict) -> str:
        if args[0] == ['networksetup', '-listallhardwareports']:
            return f"\nHardware Port: Wi-Fi\nDevice: {device_name}\n"
        else:
            assert args[0] == ['networksetup', '-setairportpower', device_name, ('on' if on else 'off')]
            return ''
    device_name = next_alphabetic(10)
    mock_parse_argv(MODULE_NAME, 'Wifi', monkeypatch)
    monkeypatch.setattr(f"{MODULE_NAME}.execute_cmd", mock_execute_cmd)
    mute_logs(MODULE_NAME, monkeypatch)
    assert Wifi().set_wifi(on) == ''
