from typing import List


def mock_parse_argv(module_name, class_name, monkeypatch, argv: List[str] = None) -> None:
    """
    Mocks the call to `parse_argv` method in the `Automation` class implementations.
    @param module_name: name of the module being tested
    @param class_name: name of the class that implements the `parse_argv` method
    @param monkeypatch: instance of `monkeypatch` of the given test
    @param argv: optional arguments vector to be set in the `Automation` instance
    """
    monkeypatch.setattr(f"{module_name}.{class_name}.parse_argv", lambda *a, **k: argv)
