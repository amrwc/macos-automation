from goodnight import Goodnight
from .testing_utils import mute_logs

MODULE_NAME = 'goodnight'


def should_have_executed(monkeypatch) -> None:
    def mock_init_common(*args: tuple, **kwargs: dict) -> None:
        assert args[1] == ['off']

    def mock_init_volume(*args: tuple, **kwargs: dict) -> None:
        assert args[1] == ['0.0']

    execute_calls = []
    monkeypatch.setattr(f"{MODULE_NAME}.Volume.__init__", mock_init_volume)
    monkeypatch.setattr(f"{MODULE_NAME}.Volume.execute", lambda *a, **k: execute_calls.append(''))
    monkeypatch.setattr(f"{MODULE_NAME}.Bluetooth.__init__", mock_init_common)
    monkeypatch.setattr(f"{MODULE_NAME}.Bluetooth.execute", lambda *a, **k: execute_calls.append(''))
    monkeypatch.setattr(f"{MODULE_NAME}.Wifi.__init__", mock_init_common)
    monkeypatch.setattr(f"{MODULE_NAME}.Wifi.execute", lambda *a, **k: execute_calls.append(''))
    monkeypatch.setattr(f"{MODULE_NAME}.Sleep.execute", lambda *a, **k: execute_calls.append(''))
    mute_logs(MODULE_NAME, monkeypatch)

    assert Goodnight().execute() == ''
    assert len(execute_calls) == 4


def should_have_printed_usage_instructions(monkeypatch) -> None:
    print_coloured_calls = []
    monkeypatch.setattr(f"{MODULE_NAME}.print_coloured", lambda *a, **k: print_coloured_calls.append(''))
    Goodnight().usage()
    assert len(print_coloured_calls) == 2
