import pytest


from testing_utils import (
    mute_logs,
    next_alphanumeric,
)
from sleep import (
    main,
)

MODULE_NAME: str = 'sleep'


def should_have_raised_error_for_wrong_result(monkeypatch) -> None:
    def mock_raise_error(*args: tuple, **kwargs: dict) -> None:
        raise SystemExit(0)  # Controlled early exit

    def mock_execute_cmd(*args: tuple, **kwargs: dict) -> str:
        assert args[0] == ['pmset', 'sleepnow']
        return next_alphanumeric(10)

    monkeypatch.setattr(f"{MODULE_NAME}.execute_cmd", mock_execute_cmd)
    monkeypatch.setattr(f"{MODULE_NAME}.raise_error", mock_raise_error)
    mute_logs(MODULE_NAME, monkeypatch)
    with pytest.raises(SystemExit) as e:
        main()
    assert e.type == SystemExit
    assert e.value.code == 0


def should_have_run_uninterrupted(monkeypatch) -> None:
    def mock_execute_cmd(*args: tuple, **kwargs: dict) -> str:
        assert args[0] == ['pmset', 'sleepnow']
        return 'Sleeping now...\n'
    monkeypatch.setattr(f"{MODULE_NAME}.execute_cmd", mock_execute_cmd)
    mute_logs(MODULE_NAME, monkeypatch)
    main()
