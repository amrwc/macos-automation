import random
import string


def next_alphabetic(length: int) -> str:
    """
    Returns random string consisting of upper and lower-case characters.
    @param length: size of the string
    @return: random alphabetic string
    """
    letters: str = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


def next_alphanumeric(length: int) -> str:
    """
    Returns random string consisting of numbers and upper and lower-case characters.
    @param length: size of the string
    @return: random alphanumeric string
    """
    letters_and_numbers: str = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_numbers) for i in range(length))
