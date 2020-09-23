"""
Common utitilies.
"""

import datetime
import subprocess
from sys import exit, stdout
from typing import Callable, Dict, List


def raise_error(message: str, cmd: List[str] = [], usage: Callable[[], None] = None) -> None:
    """
    Prints the given error message and exits with a non-zero code.
    @param message: error message
    @param cmd: optional command to be displayed as a reference
    """
    print_coloured(f"[{get_time()}] ", 'white')
    print_coloured('ERROR: ', 'red', 'bold')
    if cmd:
        print_coloured(f"{message}\n", 'red')
        print_cmd(cmd)
        print('')
    else:
        print_coloured(f"{message}\n", 'red')
    if usage:
        usage()
    exit(1)


def log(message: str) -> None:
    """
    Logs the given message to the command line.
    @param message: log message to be displayed
    """
    print_coloured(f"[{get_time()}] {message}\n", 'white')


def print_cmd(cmd: List[str]) -> None:
    """
    Prints the given command to the command line.
    @param cmd: command-line directive in a form of a list
    """
    print_coloured(f"{' '.join(cmd)}\n", 'grey')


def get_time() -> str:
    """
    Returns current time.
    @return: time in HH:MM:SS format
    """
    return datetime.datetime.now().strftime('%H:%M:%S')


def print_coloured(text: str, colour: str, effect: str = '') -> None:
    """
    Prints the given text in the given colour and effect.
    @param text: message to print out
    @param colour: display colour
    @param effect: (optional) effect to use, such as 'bold' or 'underline'
    """
    text_effect: str = get_text_effect(effect)
    stdout.write(f"{text_effect}{get_colour(colour)}{text}{get_text_effect('reset')}")


def get_colour(colour: str) -> str:
    """
    Returns an ANSI escape sequence for the given colour.
    @param colour: name of the colour
    @return: escape sequence for the given colour
    """
    sequence_base: str = '\033['
    colours: Dict[str, str] = {
        'red': '31m',
        'yellow': '33m',
        'green': '32m',
        'blue': '34m',
        'grey': '37m',
        'white': '97m'
    }
    return f"{sequence_base}{colours[colour]}"


def get_text_effect(effect: str) -> str:
    """
    Returns an ASCII escape sequence for a text effect, such as 'bold'.
    @param effect: name of the effect
    @return: escape sequence for the given effect
    """
    sequence_base: str = '\033['
    effects: Dict[str, str] = {
        '': '',
        'reset': '0m',
        'bold': '1m',
        'underline': '4m'
    }
    return f"{sequence_base}{effects[effect]}"


def execute_cmd(cmd: List[str]) -> str:
    """
    Executes the given shell command.
    @param cmd: shell directive to execute
    @return: UTF-8-decoded standard output (stdout) of the command
    """
    try:
        return subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf8')
    except subprocess.CalledProcessError:
        raise_error('Exception occurred while running the following command:', cmd)
    except KeyboardInterrupt:
        print_coloured(f"\n[{get_time()}] ", 'white')
        print_coloured('KeyboardInterrupt: ', 'yellow', 'bold')
        print_coloured('User halted the execution of the following command:\n', 'yellow')
        print_cmd(cmd)
        exit(1)
