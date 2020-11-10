import random
import string


def next_alphabetic(length: int) -> str:
    """Returns random string consisting of upper and lower-case characters.

    Args:
        length (int): Size of the string.

    Returns:
        Random alphabetic string.
    """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def next_alphanumeric(length: int) -> str:
    """Returns random string consisting of numbers and upper and lower-case characters.

    Args:
        length (int): Size of the string.

    Returns:
        Random alphanumeric string.
    """
    letters_and_numbers = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_numbers) for _ in range(length))


def mute_logs(module_name: str, monkeypatch) -> None:
    """Mutes logs.

    Utility method that (monkey)patches calls to `log()` function to prevent them from printing any output.

    Args:
        module_name (str): Name of the module that imports the `log()` function.
        monkeypatch: The given test's `monkeypatch` instance.
    """
    monkeypatch.setattr(f"{module_name}.log", lambda *a, **k: None)
