from testing_utils import (
    mute_logs,
)

from hello import Hello

MODULE_NAME: str = 'hello'


def should_have_executed(monkeypatch) -> None:
    def mock_init(*args: tuple, **kwargs: dict) -> None:
        assert args[1] == ['on']

    execute_calls: list = []
    monkeypatch.setattr(f"{MODULE_NAME}.Bluetooth.__init__", mock_init)
    monkeypatch.setattr(f"{MODULE_NAME}.Bluetooth.execute", lambda *a, **k: execute_calls.append(''))
    monkeypatch.setattr(f"{MODULE_NAME}.Wifi.__init__", mock_init)
    monkeypatch.setattr(f"{MODULE_NAME}.Wifi.execute", lambda *a, **k: execute_calls.append(''))
    mute_logs(MODULE_NAME, monkeypatch)

    result: str = Hello().execute()
    assert result == ''
    assert len(execute_calls) == 2


def should_have_printed_usage_instructions(monkeypatch) -> None:
    print_coloured_calls: list = []
    monkeypatch.setattr(f"{MODULE_NAME}.print_coloured", lambda *a, **k: print_coloured_calls.append(''))
    Hello().usage()
    assert len(print_coloured_calls) == 2
