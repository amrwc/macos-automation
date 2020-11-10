from typing import List


def mock_parse_argv(module_name: str, class_name: str, monkeypatch, argv: List[str] = None) -> None:
    """Mocks the call to `parse_argv` method in the `Automation` class implementations.

    Args:
        module_name (str): Name of the module being tested.
        class_name (str): Name of the class that implements the `parse_argv` method.
        monkeypatch: The given test's `monkeypatch` instance.
        argv (list): Optional arguments vector to be set in the `Automation` instance.
    """
    monkeypatch.setattr(f"{module_name}.{class_name}.parse_argv", lambda *a, **k: argv)
