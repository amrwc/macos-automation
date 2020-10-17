import pytest
from typing import List
from unittest.mock import patch, mock_open

from testing_utils import mute_logs, next_alphabetic, next_alphanumeric
from testing_automation_common import mock_parse_argv
from tunnelblick import Tunnelblick

MODULE_NAME = 'tunnelblick'
CONFIG = {
    'configuration-name': 'example-name',
}


@pytest.mark.parametrize('argv', [
    (['connect']),
    (['quit']),
])
def should_have_executed(monkeypatch, argv: List[str]) -> None:
    def mock_execute_cmd(*args: tuple, **kwargs: dict) -> str:
        assert args[0] == ['osascript', '-e', apple_script]
        return 'true\n'
    apple_script = next_alphanumeric(20)
    mock_parse_argv(MODULE_NAME, 'Tunnelblick', monkeypatch, argv)
    monkeypatch.setattr(f"{MODULE_NAME}.Tunnelblick.get_config", lambda *a, **k: CONFIG)
    monkeypatch.setattr(f"{MODULE_NAME}.Tunnelblick.build_apple_script", lambda *a, **k: apple_script)
    monkeypatch.setattr(f"{MODULE_NAME}.execute_cmd", mock_execute_cmd)
    mute_logs(MODULE_NAME, monkeypatch)
    assert Tunnelblick().execute() == 'true'


@pytest.mark.parametrize('argv', [
    ([next_alphabetic(10)]),
    ([]),
])
def should_not_have_parsed_argv_with_wrong_or_no_option(monkeypatch, argv: List[str]) -> None:
    def mock_raise_error(*args: tuple, **kwargs: dict) -> None:
        assert kwargs['usage'] is not None
        raise SystemExit(0)  # Controlled early exit
    monkeypatch.setattr(f"{MODULE_NAME}.raise_error", mock_raise_error)
    with pytest.raises(SystemExit) as e:
        Tunnelblick(argv)
    assert e.type == SystemExit
    assert e.value.code == 0


@pytest.mark.parametrize('argv', [
    (['connect']),
    (['quit']),
])
def should_have_parsed_argv(argv: List[str]) -> None:
    assert Tunnelblick(argv).argv == argv


def should_have_printed_usage_instructions(monkeypatch) -> None:
    print_coloured_calls = []
    mock_parse_argv(MODULE_NAME, 'Tunnelblick', monkeypatch)
    monkeypatch.setattr(f"{MODULE_NAME}.print_coloured", lambda *a, **k: print_coloured_calls.append(''))
    Tunnelblick().usage()
    assert len(print_coloured_calls) == 2


def should_not_have_gotten_config_when_the_file_doesnt_exist(monkeypatch) -> None:
    def mock_isfile(*args: tuple, **kwargs: dict) -> bool:
        assert args[0] == config_path
        return False

    def mock_raise_error(*args: tuple, **kwargs: dict) -> None:
        assert config_path in args[0]
        raise SystemExit(0)  # Controlled early exit

    config_path = next_alphabetic(16)
    mock_parse_argv(MODULE_NAME, 'Tunnelblick', monkeypatch)
    monkeypatch.setattr(f"{MODULE_NAME}.os.path.isfile", mock_isfile)
    monkeypatch.setattr(f"{MODULE_NAME}.raise_error", mock_raise_error)

    with pytest.raises(SystemExit) as e:
        Tunnelblick().get_config(config_path)
    assert e.type == SystemExit
    assert e.value.code == 0


def should_have_gotten_config(monkeypatch) -> None:
    def mock_isfile(*args: tuple, **kwargs: dict) -> bool:
        assert args[0] == config_path
        return True
    config_path = next_alphabetic(16)
    mock_parse_argv(MODULE_NAME, 'Tunnelblick', monkeypatch)
    monkeypatch.setattr(f"{MODULE_NAME}.os.path.isfile", mock_isfile)
    monkeypatch.setattr(f"{MODULE_NAME}.json.load", lambda *a, **k: CONFIG)
    with patch('builtins.open', mock_open(read_data='data')):
        assert Tunnelblick().get_config(config_path) == CONFIG


def should_have_built_apple_script(monkeypatch) -> None:
    instruction = next_alphanumeric(10)
    mock_parse_argv(MODULE_NAME, 'Tunnelblick', monkeypatch)
    expected_result = '\n'.join(('tell application "/Applications/Tunnelblick.app"', instruction, 'end tell'))
    assert Tunnelblick().build_apple_script(instruction) == expected_result
