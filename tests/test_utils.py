import subprocess
from typing import List

import pytest

import utils
from .testing_utils import next_alphabetic, next_alphanumeric

MODULE_NAME = 'utils'


@pytest.mark.parametrize('message, cmd, usage_present', [
    (next_alphabetic(10), [next_alphanumeric(16)], True),
    (next_alphabetic(10), [next_alphanumeric(16)], False),
    (next_alphabetic(10), [], True),
    (next_alphabetic(10), [], False),
])
def should_have_raised_error(monkeypatch, message: str, cmd: List[str], usage_present: bool) -> None:
    def mock_print_cmd(*args: tuple, **kwargs: dict) -> None:
        assert args[0] == cmd

    print_coloured_calls = []
    monkeypatch.setattr(f"{MODULE_NAME}.print_coloured", lambda *a, **k: print_coloured_calls.append(a))
    monkeypatch.setattr(f"{MODULE_NAME}.print_cmd", mock_print_cmd)

    usage_calls = []
    with pytest.raises(SystemExit) as e:
        utils.raise_error(message, usage=((lambda: usage_calls.append('')) if usage_present else None))
    assert e.type == SystemExit
    assert e.value.code == 1
    assert len(print_coloured_calls) == 3
    assert message in print_coloured_calls[2][0]
    assert len(usage_calls) == (1 if usage_present else 0)


def should_have_logged_message(monkeypatch) -> None:
    print_coloured_calls = []
    monkeypatch.setattr(f"{MODULE_NAME}.print_coloured", lambda *a, **k: print_coloured_calls.append(a))
    message = next_alphabetic(10)
    utils.log(message)
    assert len(print_coloured_calls) == 1
    assert message in print_coloured_calls[0][0]


@pytest.mark.parametrize('cmd', [
    ([next_alphanumeric(16)]),
    ([next_alphanumeric(16), next_alphanumeric(16)]),
])
def should_have_printed_cmd(monkeypatch, cmd: List[str]) -> None:
    print_coloured_calls = []
    monkeypatch.setattr(f"{MODULE_NAME}.print_coloured", lambda *a, **k: print_coloured_calls.append(a))
    utils.print_cmd(cmd)
    assert ' '.join(cmd) in print_coloured_calls[0][0]


def should_have_handled_exception_during_executing_cmd(monkeypatch) -> None:
    def mock_run(*args: tuple, **kwargs: dict) -> None:
        raise subprocess.CalledProcessError('', '')

    def mock_raise_error(*args: tuple, **kwargs: dict) -> None:
        assert args[1] == cmd

    monkeypatch.setattr(f"{MODULE_NAME}.subprocess.run", mock_run)
    monkeypatch.setattr(f"{MODULE_NAME}.raise_error", mock_raise_error)

    cmd = [next_alphabetic(10), next_alphanumeric(16)]
    utils.execute_cmd(cmd)


def should_have_handled_keyboard_interrupt_during_executing_cmd(monkeypatch) -> None:
    def mock_run(*args: tuple, **kwargs: dict) -> None:
        raise KeyboardInterrupt('', '')

    def mock_print_cmd(*args: tuple, **kwargs: dict) -> None:
        assert args[0] == cmd

    monkeypatch.setattr(f"{MODULE_NAME}.subprocess.run", mock_run)
    monkeypatch.setattr(f"{MODULE_NAME}.print_coloured", lambda *a, **k: None)
    monkeypatch.setattr(f"{MODULE_NAME}.print_cmd", mock_print_cmd)

    cmd = [next_alphabetic(10), next_alphanumeric(16)]
    with pytest.raises(SystemExit) as e:
        utils.execute_cmd(cmd)
    assert e.type == SystemExit
    assert e.value.code == 1


def should_have_executed_cmd(monkeypatch) -> None:
    def mock_run(*args: tuple, **kwargs: dict):
        class MockResult:
            stdout = b'SUCCESS'
        return MockResult()

    monkeypatch.setattr(f"{MODULE_NAME}.subprocess.run", mock_run)
    raise_error_calls = []
    monkeypatch.setattr(f"{MODULE_NAME}.raise_error", lambda *a, **k: raise_error_calls.append(''))
    print_cmd_calls = []
    monkeypatch.setattr(f"{MODULE_NAME}.print_cmd", lambda *a, **k: print_cmd_calls.append(''))

    cmd = [next_alphabetic(10), next_alphanumeric(16)]
    assert utils.execute_cmd(cmd) == 'SUCCESS'
    assert len(raise_error_calls) == 0
    assert len(print_cmd_calls) == 0
