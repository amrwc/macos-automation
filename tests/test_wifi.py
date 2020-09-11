import pytest
from typing import List

from testing_utils import (
    mute_logs,
    next_alphabetic,
    next_alphanumeric,
)
from wifi import (
    main,
    set_wifi,
    usage,
)


MODULE_NAME: str = 'wifi'


@pytest.mark.parametrize('argv, raised_error', [
    ([f"{MODULE_NAME}.py"], True),
    ([f"{MODULE_NAME}.py", next_alphanumeric(10)], True),
])
def should_have_raised_error_for_unknown_option(monkeypatch, argv: List[str], raised_error: bool) -> None:
    def mock_raise_error(*args: tuple, **kwargs: dict) -> None:
        assert kwargs['usage'] == usage
        raise_error_calls.append('')
        raise SystemExit(0)  # Controlled early exit
    raise_error_calls: list = []
    monkeypatch.setattr(f"{MODULE_NAME}.sys.argv", argv)
    monkeypatch.setattr(f"{MODULE_NAME}.raise_error", mock_raise_error)
    with pytest.raises(SystemExit) as e:
        main()
    assert e.type == SystemExit
    assert e.value.code == 0
    raise_error_calls == 1


@pytest.mark.parametrize('argv', [
    ([f"{MODULE_NAME}.py", 'on']),
    ([f"{MODULE_NAME}.py", 'off']),
])
def should_have_run_uninterrupted(monkeypatch, argv: List[str]) -> None:
    def mock_set_wifi(*args: tuple, **kwargs: dict) -> None:
        assert args[0] == (argv[1] == 'on')
    monkeypatch.setattr(f"{MODULE_NAME}.sys.argv", argv)
    monkeypatch.setattr(f"{MODULE_NAME}.set_wifi", mock_set_wifi)
    main()


@pytest.mark.parametrize('on', [(True), (False)])
def should_have_set_wifi(monkeypatch, on) -> None:
    def mock_execute_cmd(*args: tuple, **kwargs: dict) -> None:
        if args[0] == ['networksetup', '-listallhardwareports']:
            return f"\nHardware Port: Wi-Fi\nDevice: {device_name}\n"
        else:
            assert args[0] == ['networksetup', '-setairportpower', device_name, ('on' if on else 'off')]
    device_name: str = next_alphabetic(10)
    monkeypatch.setattr(f"{MODULE_NAME}.execute_cmd", mock_execute_cmd)
    mute_logs(MODULE_NAME, monkeypatch)
    set_wifi(on)


def should_have_printed_usage_instructions(monkeypatch) -> None:
    print_coloured_calls: list = []
    monkeypatch.setattr(f"{MODULE_NAME}.print_coloured", lambda *a, **k: print_coloured_calls.append(''))
    usage()
    assert len(print_coloured_calls) == 2
