import pytest
import random
from typing import List

from testing_utils import (
    mute_logs,
    next_alphanumeric,
)
from testing_automation_common import (
    mock_parse_argv,
)
from brightness import Brightness


MODULE_NAME: str = 'brightness'


def should_have_executed(monkeypatch) -> None:
    def mock_execute_cmd(*args: tuple, **kwargs: dict) -> str:
        assert args[0] == ['brightness', brightness_level]
        return expected_result

    mock_parse_argv(MODULE_NAME, 'Brightness', monkeypatch)
    mute_logs(MODULE_NAME, monkeypatch)
    monkeypatch.setattr(f"{MODULE_NAME}.execute_cmd", mock_execute_cmd)

    brightness_level: str = str(random.random())
    expected_result: str = next_alphanumeric(10)
    automation: Brightness = Brightness()
    automation.brightness = brightness_level
    assert automation.execute() == expected_result


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
        Brightness(argv)
    assert e.type == SystemExit
    assert e.value.code == 0


@pytest.mark.parametrize('argv', [
    (['-5.7']),
    (['0.0']),
    (['0.5']),
    (['1.0']),
    (['3.2']),
])
def should_have_parsed_argv(argv) -> None:
    brightness: Brightness = Brightness(argv)
    assert brightness.argv == argv


def should_have_printed_usage_instructions(monkeypatch) -> None:
    print_coloured_calls: list = []
    mock_parse_argv(MODULE_NAME, 'Brightness', monkeypatch)
    monkeypatch.setattr(f"{MODULE_NAME}.print_coloured", lambda *a, **k: print_coloured_calls.append(''))
    Brightness().usage()
    assert len(print_coloured_calls) == 2
