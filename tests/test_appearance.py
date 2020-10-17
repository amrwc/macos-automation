import pytest
from typing import List

from testing_utils import mute_logs, next_alphabetic, next_alphanumeric
from testing_automation_common import mock_parse_argv
from appearance import Appearance

MODULE_NAME = 'appearance'


@pytest.mark.parametrize('argv, current_mode', [
    (['dark'], 'light'),
    (['dark'], 'dark'),
    (['light'], 'dark'),
    (['light'], 'light'),
    (['toggle', next_alphabetic(16)]),
])
def should_have_executed(monkeypatch, argv: List[str], current_mode: str) -> None:
    def mock_tell_appearance_preferences(*args: tuple, **kwargs: dict) -> str:
        tell_appearance_preferences_calls.append('')
        return ''
    mock_parse_argv(MODULE_NAME, 'Appearance', monkeypatch, argv)
    monkeypatch.setattr(f"{MODULE_NAME}.Appearance.get_current_mode", lambda *a, **k: current_mode)
    tell_appearance_preferences_calls = []
    monkeypatch.setattr(f"{MODULE_NAME}.Appearance.tell_appearance_preferences", mock_tell_appearance_preferences)
    mute_logs(MODULE_NAME, monkeypatch)

    appearance = Appearance()
    appearance.toggle = argv[0] == 'toggle'
    if not appearance.toggle:
        appearance.mode = argv[0]
    assert appearance.execute() == ''
    if appearance.mode:
        assert len(tell_appearance_preferences_calls) == 0 if appearance.mode == current_mode else 1
    else:
        assert len(tell_appearance_preferences_calls) == 1


@pytest.mark.parametrize('argv', [
    ([next_alphabetic(16)]),
    ([]),
])
def should_not_have_parsed_argv_with_wrong_or_no_option(monkeypatch, argv: List[str]) -> None:
    def mock_raise_error(*args: tuple, **kwargs: dict) -> None:
        assert kwargs['usage'] is not None
        raise SystemExit(0)  # Controlled early exit
    monkeypatch.setattr(f"{MODULE_NAME}.raise_error", mock_raise_error)
    with pytest.raises(SystemExit) as e:
        Appearance(argv)
    assert e.type == SystemExit
    assert e.value.code == 0


@pytest.mark.parametrize('argv', [
    (['dark']),
    (['light']),
    (['toggle']),
])
def should_have_parsed_argv(argv: List[str]) -> None:
    appearance = Appearance(argv)
    assert appearance.argv == []
    is_toggle = argv[0] == 'toggle'
    assert appearance.toggle == is_toggle
    if is_toggle:
        assert appearance.mode is None
    else:
        assert appearance.mode == argv[0]


def should_have_printed_usage_instructions(monkeypatch) -> None:
    print_coloured_calls = []
    mock_parse_argv(MODULE_NAME, 'Appearance', monkeypatch)
    monkeypatch.setattr(f"{MODULE_NAME}.print_coloured", lambda *a, **k: print_coloured_calls.append(''))
    Appearance().usage()
    assert len(print_coloured_calls) == 2


def should_have_gotten_current_mode(monkeypatch) -> None:
    def mock_tell_appearance_preferences(*args: tuple, **kwargs: dict) -> str:
        tell_appearance_preferences_calls.append('')
        return current_mode
    tell_appearance_preferences_calls = []
    current_mode = next_alphanumeric(16)
    monkeypatch.setattr(f"{MODULE_NAME}.Appearance.tell_appearance_preferences", mock_tell_appearance_preferences)
    mock_parse_argv(MODULE_NAME, 'Appearance', monkeypatch)
    assert Appearance().get_current_mode() == current_mode


def should_have_executed_the_given_apple_script_on_appearance_preferences(monkeypatch) -> None:
    def mock_execute_cmd(*args: tuple, **kwargs: dict) -> str:
        assert apple_script[0] in args[0][2]
        return result
    result = next_alphanumeric(16)
    monkeypatch.setattr(f"{MODULE_NAME}.execute_cmd", mock_execute_cmd)
    mock_parse_argv(MODULE_NAME, 'Appearance', monkeypatch)
    apple_script = (next_alphanumeric(16),)
    assert Appearance().tell_appearance_preferences(apple_script) == result
