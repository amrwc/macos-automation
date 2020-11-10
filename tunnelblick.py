#!/usr/bin/env python3

"""
# Tunnelblick

A utility for sending simple instructions to Tunnelblick from command line.

Supported commands:

- connect -- opens Tunnelblick if it was closed and establishes a connection using the configuration specified in the
  config file.
- quit -- quits Tunnelblick.

## Setup

1. Rename `tunnelblick.config.example.json` to `tunnelblick.config.json`.
2. Set `configuration-name` field to the VPN configuration name already imported to Tunnelblick.
3. Create a symlink to the script:

   ```console
   ln -s "$(pwd)/tunnelblick.py" /usr/local/bin/tunnelblick
   ```

## Usage

```console
tunnelblick <connect/quit>
```

@author: amrwc
"""

import json
import os
import sys
from typing import Dict, List

from abstract_automation import Automation
from utils import (
    execute_cmd,
    log,
    print_coloured,
    raise_error,
)

CONFIG_FILE_NAME = 'tunnelblick.config.json'
SCRIPT_PARENT_DIR_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
CONFIG_FILE_PATH = f"{SCRIPT_PARENT_DIR_PATH}/{CONFIG_FILE_NAME}"


class Tunnelblick(Automation):

    def __init__(self, argv: List[str] = []):
        self.argv = self.parse_argv(argv)

    def execute(self) -> str:
        config = self.get_config(CONFIG_FILE_PATH)
        instructions = {
            'connect': f"connect \"{config['configuration-name']}\"",
            'quit': 'quit',
        }
        instruction = instructions[self.argv[0]]
        apple_script = self.build_apple_script(instruction)
        log(f"Instructing Tunnelblick to {instruction}")
        return execute_cmd(['osascript', '-e', apple_script]).strip()

    def parse_argv(self, argv: List[str]) -> List[str]:
        if len(argv) == 0:
            raise_error('No option provided', usage=self.usage)
        if argv[0] not in ('connect', 'quit'):
            raise_error(f"Unsupported option provided: {argv[0]}", usage=self.usage)
        return argv

    def usage(self) -> None:
        print_coloured('Usage:\n', 'white', 'bold')
        print_coloured('$ ./tunnelblick.py <connect/quit>\n', 'white')

    def get_config(self, config_path: str) -> Dict[str, str]:
        """Fetches config file contents.

        Returns config file contents as a dictionary or raises an error if the file doesn't exist.

        Args:
            config_path: Path to the config file.

        Returns:
            Config file contents in a dictionary.
        """
        if not os.path.isfile(config_path):
            raise_error(f"The config file doesn't exist in '{config_path}'")
        with open(config_path) as config_file:
            return json.load(config_file)

    def build_apple_script(self, instruction: str) -> str:
        """Builds an AppleScript snippet that passes commands into Tunnelblick.

        Args:
            instruction: Command for Tunnelblick.

        Returns:
            An AppleScript (osascript) snippet.
        """
        return '\n'.join(('tell application "/Applications/Tunnelblick.app"', instruction, 'end tell'))


if __name__ == '__main__':
    result = Tunnelblick(sys.argv[1:]).execute()
    if result not in ('true', '0'):
        raise_error(f"Something went wrong; stdout: {result}")
