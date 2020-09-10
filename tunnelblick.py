#!/usr/bin/env python3

"""
Tunnelblick

A utility for sending simple instructions to Tunnelblick from command line.

Supported commands:
- connect -- opens Tunnelblick if it was closed and establishes a connection using the configuration specified in the
  config file.
- quit -- quits Tunnelblick.

Usage:
1. Rename `tunnelblick.config.example.json` to `tunnelblick.config.json`.
2. Set `configuration-name` field to the VPN configuration name already imported to Tunnelblick.
3. Run the following:

   ```console
   $ ./tunnelblick.py <connect/quit>
   ```

@author amrwc
"""

import json
import os
import sys
from typing import Dict, List
from utils import (
    execute_cmd,
    log,
    print_coloured,
    raise_error,
)


CONFIG_FILE_NAME: str = 'tunnelblick.config.json'
SCRIPT_PARENT_DIR_PATH: str = os.path.dirname(os.path.realpath(sys.argv[0]))
CONFIG_FILE_PATH: str = f"{SCRIPT_PARENT_DIR_PATH}/{CONFIG_FILE_NAME}"


def main() -> None:
    """
    The application's entry point.
    """
    argv: List[str] = parse_argv()
    config: Dict[str, str] = get_config(CONFIG_FILE_PATH)
    instructions: Dict[str, str] = {
        'connect': f"connect \"{config['configuration-name']}\"",
        'quit': 'quit',
    }
    instruction: str = instructions[argv[0]]
    apple_script: str = build_apple_script(instruction)
    log(f"Instructing Tunnelblick to {instruction}")
    stdout: str = execute_cmd(['osascript', '-e', apple_script])
    if stdout not in ('true\n', '0\n'):
        raise_error(f"Something went wrong; stdout: {stdout}")


def parse_argv() -> List[str]:
    """
    Parses and verifies the command-line arguments and returns them with the script name removed.
    @return: command-line arguments
    """
    argv: List[str] = sys.argv[1:]
    if len(argv) == 0:
        raise_error('No option provided', usage=usage)
    if argv[0] not in ('connect', 'quit'):
        raise_error(f"Unsupported option provided: {argv[0]}", usage=usage)
    return argv


def get_config(config_path: str) -> Dict[str, str]:
    """
    Returns the config file contents as a dictionary or raises an error if the file doesn't exist.
    @param config_path: path to the config file
    @return: config file contents
    """
    if not os.path.isfile(config_path):
        raise_error(f"The config file doesn't exist in '{config_path}'")
    with open(config_path) as config_file:
        return json.load(config_file)


def build_apple_script(instruction: str) -> str:
    """
    Returns a ready-made AppleScript snippet that passes commands into Tunnelblick.
    @param instruction: command for Tunnelblick
    @return: AppleScript (osascript) snippet
    """
    return '\n'.join(('tell application "/Applications/Tunnelblick.app"', instruction, 'end tell'))


def usage() -> None:
    """
    Prints usage instructions.
    """
    print_coloured('Usage:\n', 'white', 'bold')
    print_coloured('$ ./tunnelblick.py <connect/quit>\n', 'white')


if __name__ == '__main__':
    main()
