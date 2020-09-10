import pytest
import subprocess
from typing import List

from testing_utils import (
    next_alphabetic,
    next_alphanumeric,
)
from utils import (
    raise_error,
    print_cmd,
    log,
    execute_cmd,
)


@pytest.mark.parametrize('message, cmd, usage_present', [
    (next_alphabetic(10), [next_alphanumeric(16)], True),
    (next_alphabetic(10), [next_alphanumeric(16)], False),
    (next_alphabetic(10), [], True),
    (next_alphabetic(10), [], False),
])
def should_have_raised_error(monkeypatch, message: str, cmd: List[str], usage_present: bool) -> None:
    def mock_print_cmd(*args: tuple, **kwargs: dict):
        assert args == (cmd,)

    def mock_usage():
        usage_calls.append('')

    print_coloured_calls: List[str] = []
    monkeypatch.setattr('utils.print_coloured', lambda *a, **k: print_coloured_calls.append(a))
    monkeypatch.setattr('utils.print_cmd', mock_print_cmd)
    usage_calls: List[str] = []

    with pytest.raises(SystemExit) as e:
        raise_error(message, usage=(mock_usage if usage_present else None))
    assert e.type == SystemExit
    assert e.value.code == 1
    assert len(print_coloured_calls) == 3
    assert message in print_coloured_calls[2][0]
    assert len(usage_calls) == (1 if usage_present else 0)


def should_have_logged_message(monkeypatch) -> None:
    message: str = next_alphabetic(10)
    print_coloured_calls: List[str] = []
    monkeypatch.setattr('utils.print_coloured', lambda *a, **k: print_coloured_calls.append(a))

    log(message)
    assert len(print_coloured_calls) == 1
    assert message in print_coloured_calls[0][0]


@pytest.mark.parametrize('cmd', [
    ([next_alphanumeric(16)]),
    ([next_alphanumeric(16), next_alphanumeric(16)]),
])
def should_have_printed_cmd(monkeypatch, cmd: List[str]) -> None:
    print_coloured_calls: List[str] = []
    monkeypatch.setattr('utils.print_coloured', lambda *a, **k: print_coloured_calls.append(a))
    print_cmd(cmd)
    assert ' '.join(cmd) in print_coloured_calls[0][0]


def should_have_handled_exception_during_executing_cmd(monkeypatch) -> None:
    cmd: List[str] = [next_alphabetic(10), next_alphanumeric(16)]

    def mock_run(*args: tuple, **kwargs: dict):
        raise subprocess.CalledProcessError('', '')

    def mock_raise_error(*args: tuple, **kwargs: dict):
        assert args[1] == cmd

    monkeypatch.setattr('utils.subprocess.run', mock_run)
    monkeypatch.setattr('utils.raise_error', mock_raise_error)
    execute_cmd(cmd)


def should_have_handled_keyboard_interrupt_during_executing_cmd(monkeypatch) -> None:
    cmd: List[str] = [next_alphabetic(10), next_alphanumeric(16)]

    def mock_run(*args: tuple, **kwargs: dict):
        raise KeyboardInterrupt('', '')

    def mock_print_cmd(*args: tuple, **kwargs: dict):
        assert args == (cmd,)

    monkeypatch.setattr('utils.subprocess.run', mock_run)
    monkeypatch.setattr('utils.print_coloured', lambda *a, **k: None)
    monkeypatch.setattr('utils.print_cmd', mock_print_cmd)

    with pytest.raises(SystemExit) as e:
        execute_cmd(cmd)
    assert e.type == SystemExit
    assert e.value.code == 1


def should_have_executed_cmd(monkeypatch) -> None:
    cmd: List[str] = [next_alphabetic(10), next_alphanumeric(16)]

    def mock_run(*args: tuple, **kwargs: dict):
        class MockResult:
            stdout = b'SUCCESS'
        return MockResult()

    monkeypatch.setattr('utils.subprocess.run', mock_run)
    raise_error_calls: List[str] = []
    monkeypatch.setattr('utils.raise_error', lambda *a, **k: raise_error_calls.append(''))
    print_cmd_calls: List[str] = []
    monkeypatch.setattr('utils.print_cmd', lambda *a, **k: print_cmd_calls.append(''))

    assert execute_cmd(cmd) == 'SUCCESS'
    assert len(raise_error_calls) == 0
    assert len(print_cmd_calls) == 0
