#!/usr/bin/env python3

"""
# Bluetooth

A utility for turning Bluetooth on/off from command-line.

## Setup

1. Install Blueutil:

   ```console
   brew install blueutil
   ```

2. Create a symlink to the script.

   ```console
   ln -s "$(pwd)/bluetooth.py" /usr/local/bin/bluetooth
   ```

## Usage

```console
bluetooth <on/off>
```

@author: amrwc
"""

import sys
from typing import List

from abstract_automation import Automation
from utils import (
    execute_cmd,
    log,
    print_coloured,
    raise_error,
)


# def main(argv: List[str] = []) -> None:
#     """
#     The application's entry point.
#     """
#     if not argv:
#         argv = sys.argv[1:]
#     if len(argv) == 0:
#         raise_error('No option provided', usage=usage)
#     option: str = argv[0]
#     if option not in ('on', 'off',):
#         raise_error(f"Unsupported option provided: {option}", usage=usage)
#     set_bluetooth(option == 'on')


# def set_bluetooth(on: bool) -> None:
#     """
#     Runs a `blueutil` command and turns Bluetooth to the given state.
#     @param on: whether to turn Bluetooth on
#     """
#     power: str = '1' if on else '0'
#     log(f"Turning Bluetooth {'on' if on else 'off'}")
#     execute_cmd(['blueutil', '-p', power])


# def usage() -> None:
#     """
#     Prints usage instructions.
#     """
#     print_coloured('Usage:\n', 'white', 'bold')
#     print_coloured('$ ./bluetooth.py <on/off>\n', 'white')


class Bluetooth(Automation):

    def __init__(self, argv: List[str] = []):
        self.argv = self.parse_argv(argv)

    def execute(self) -> str:
        return self.set_bluetooth(self.argv[0] == 'on')

    def parse_argv(self, argv: List[str]) -> List[str]:
        if len(argv) == 0:
            raise_error('No option provided', usage=self.usage)
        if argv[0] not in ('on', 'off'):
            raise_error(f"Unsupported option provided: {argv[0]}", usage=self.usage)
        return argv

    def usage(self) -> None:
        print_coloured('Usage:\n', 'white', 'bold')
        print_coloured('$ ./bluetooth.py <on/off>\n', 'white')

    def set_bluetooth(self, on: bool) -> None:
        """
        Runs a `blueutil` command and turns Bluetooth to the given state.
        @param on: whether to turn Bluetooth on
        """
        power: str = '1' if on else '0'
        log(f"Turning Bluetooth {'on' if on else 'off'}")
        return execute_cmd(['blueutil', '-p', power]).strip()


if __name__ == '__main__':
    result: str = Bluetooth(sys.argv[1:]).execute()
    if result != '':
        raise_error(f"Something went wrong; stdout: {result}")
