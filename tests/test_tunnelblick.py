import pytest
from typing import Dict, List
from unittest.mock import patch, mock_open

from testing_utils import (
    next_alphabetic,
    next_alphanumeric,
)
from tunnelblick import (
    parse_argv,
    get_config,
    build_apple_script,
    usage,
)


CONFIG: Dict[str, str] = {
    'configuration-name': 'example-name',
}


@pytest.mark.parametrize('argv, expected_result, raised_error', [
    (['tunnelblick.py'], None, True,),
    (['tunnelblick.py', next_alphabetic(10)], None, True,),
])
def should_have_raised_error_when_parsing_argv(
        monkeypatch,
        argv: List[str],
        expected_result: List[str],
        raised_error: bool
) -> None:
    def mock_raise_error(*args: tuple, **kwargs: dict) -> None:
        assert kwargs['usage'] == usage
        raise_error_calls.append('')
        raise SystemExit(0)  # Controlled early exit
    raise_error_calls: list = []
    monkeypatch.setattr('tunnelblick.sys.argv', argv)
    monkeypatch.setattr('tunnelblick.raise_error', mock_raise_error)

    with pytest.raises(SystemExit) as e:
        result: List[str] = parse_argv()
        assert result == expected_result
    assert e.type == SystemExit
    assert e.value.code == 0
    assert len(raise_error_calls) == (1 if raised_error else 0)


@pytest.mark.parametrize('argv, expected_result', [
    (['tunnelblick.py', 'connect'], ['connect'],),
    (['tunnelblick.py', 'quit'], ['quit'],),
])
def should_have_parsed_argv(monkeypatch, argv: List[str], expected_result: List[str]) -> None:
    monkeypatch.setattr('tunnelblick.sys.argv', argv)
    result: List[str] = parse_argv()
    assert result == expected_result


def should_not_have_gotten_config_when_the_file_doesnt_exist(monkeypatch) -> None:
    def mock_isfile(*args: tuple, **kwargs: dict) -> None:
        assert args == (config_path,)
        return False

    def mock_raise_error(*args: tuple, **kwargs: dict) -> None:
        assert config_path in args[0]
        raise SystemExit(0)  # Controlled early exit

    monkeypatch.setattr('tunnelblick.os.path.isfile', mock_isfile)
    monkeypatch.setattr('tunnelblick.raise_error', mock_raise_error)

    config_path: str = next_alphabetic(16)
    with pytest.raises(SystemExit) as e:
        get_config(config_path)
    assert e.type == SystemExit
    assert e.value.code == 0


def should_have_gotten_config(monkeypatch) -> None:
    def mock_isfile(*args: tuple, **kwargs: dict) -> None:
        assert args == (config_path,)
        return True
    monkeypatch.setattr('tunnelblick.os.path.isfile', mock_isfile)

    config_path: str = next_alphabetic(16)
    with patch('builtins.open', mock_open(read_data='data')):
        monkeypatch.setattr('tunnelblick.json.load', lambda *a, **k: CONFIG)
        assert get_config(config_path) == CONFIG


def should_have_built_apple_script() -> None:
    instruction: str = next_alphanumeric(10)
    expected_result: str = '\n'.join(('tell application "/Applications/Tunnelblick.app"', instruction, 'end tell'))
    assert build_apple_script(instruction) == expected_result


def should_have_printed_usage_instructions(monkeypatch) -> None:
    print_coloured_calls: list = []
    monkeypatch.setattr('tunnelblick.print_coloured', lambda *a, **k: print_coloured_calls.append(''))
    usage()
    assert len(print_coloured_calls) == 2
