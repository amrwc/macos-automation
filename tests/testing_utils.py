import random
import string


def next_alphabetic(length: int) -> str:
    """
    Returns random string consisting of upper and lower-case characters.
    @param length: size of the string
    @return: random alphabetic string
    """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


def next_alphanumeric(length: int) -> str:
    """
    Returns random string consisting of numbers and upper and lower-case characters.
    @param length: size of the string
    @return: random alphanumeric string
    """
    letters_and_numbers = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_numbers) for i in range(length))


def mute_logs(module_name: str, monkeypatch) -> None:
    """
    Utility method that (monkey)patches calls to `log()` function to prevent them from printing any output.
    @param module_name: name of the module that imports the `log()` function
    @param monkeypatch: the given test's instance of `monkeypatch`
    """
    monkeypatch.setattr(f"{module_name}.log", lambda *a, **k: None)
