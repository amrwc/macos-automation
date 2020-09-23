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
from volume import Volume


MODULE_NAME: str = 'volume'


def should_have_executed(monkeypatch) -> None:
    def mock_build_apple_script(*args: tuple, **kwargs: dict) -> str:
        assert args[1] == volume_level
        return apple_script

    def mock_execute_cmd(*args: tuple, **kwargs: dict) -> str:
        assert args[0] == ['osascript', '-e', apple_script]
        return f"  {expected_result}  "

    apple_script: str = next_alphanumeric(16)
    mock_parse_argv(MODULE_NAME, 'Volume', monkeypatch)
    mute_logs(MODULE_NAME, monkeypatch)
    monkeypatch.setattr(f"{MODULE_NAME}.Volume.build_apple_script", mock_build_apple_script)
    monkeypatch.setattr(f"{MODULE_NAME}.execute_cmd", mock_execute_cmd)

    volume_level: float = random.random()
    expected_result: str = next_alphanumeric(10)
    automation: Volume = Volume()
    automation.volume = volume_level
    automation.execute()


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
        Volume(argv)
    assert e.type == SystemExit
    assert e.value.code == 0


@pytest.mark.parametrize('argv, expected_volume_level', [
    (['-5.7'], 0.0),
    (['-1'], 0.0),
    (['0.0'], 0.0),
    (['0'], 0.0),
    (['0.5'], 0.5),
    (['1'], 1.0),
    (['1.0'], 1.0),
    (['3.2'], 3.2),
    (['7'], 7.0),
    (['7.0'], 7.0),
    (['8.0'], 7.0),
])
def should_have_parsed_argv(argv, expected_volume_level) -> None:
    volume: Volume = Volume(argv)
    assert volume.argv == argv
    assert volume.volume == expected_volume_level


def should_have_printed_usage_instructions(monkeypatch) -> None:
    print_coloured_calls: list = []
    mock_parse_argv(MODULE_NAME, 'Volume', monkeypatch)
    monkeypatch.setattr(f"{MODULE_NAME}.print_coloured", lambda *a, **k: print_coloured_calls.append(''))
    Volume().usage()
    assert len(print_coloured_calls) == 2


def should_have_built_apple_script(monkeypatch) -> None:
    volume: float = random.random()
    mock_parse_argv(MODULE_NAME, 'Volume', monkeypatch)
    expected_result: str = f"set Volume {str(volume)}"
    result: str = Volume().build_apple_script(volume)
    assert result == expected_result
