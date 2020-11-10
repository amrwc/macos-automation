from sleep import Sleep
from .testing_utils import mute_logs

MODULE_NAME = 'sleep'


def should_have_executed(monkeypatch) -> None:
    def mock_execute_cmd(*args: tuple, **kwargs: dict) -> str:
        assert args[0] == ['pmset', 'sleepnow']
        return 'Sleeping now...\n'
    monkeypatch.setattr(f"{MODULE_NAME}.execute_cmd", mock_execute_cmd)
    mute_logs(MODULE_NAME, monkeypatch)
    assert Sleep().execute() == 'Sleeping now...'


def should_have_printed_usage_instructions(monkeypatch) -> None:
    print_coloured_calls = []
    monkeypatch.setattr(f"{MODULE_NAME}.print_coloured", lambda *a, **k: print_coloured_calls.append(''))
    Sleep().usage()
    assert len(print_coloured_calls) == 2
