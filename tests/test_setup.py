from testing_utils import mute_logs
import setup

MODULE_NAME = 'setup'


def should_not_have_set_up_symlinks_if_they_already_exist(monkeypatch) -> None:
    mute_logs(MODULE_NAME, monkeypatch)
    monkeypatch.setattr(f"{MODULE_NAME}.os.path.islink", lambda *a, **k: True)
    symlink_calls = []
    monkeypatch.setattr(f"{MODULE_NAME}.os.symlink", lambda *a, **k: symlink_calls.append(''))
    setup.main()
    assert len(symlink_calls) == 0


def should_have_set_up_symlinks(monkeypatch) -> None:
    mute_logs(MODULE_NAME, monkeypatch)
    monkeypatch.setattr(f"{MODULE_NAME}.os.path.islink", lambda *a, **k: False)
    symlink_calls = []
    monkeypatch.setattr(f"{MODULE_NAME}.os.symlink", lambda *a, **k: symlink_calls.append(''))
    setup.main()
    assert len(symlink_calls) == 9
