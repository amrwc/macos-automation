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


class Bluetooth(Automation):

    def __init__(self, argv: List[str] = []):
        self.argv = self.parse_argv(argv)

    def execute(self) -> str:
        log(f"Turning Bluetooth {self.argv[0]}")
        on = self.argv[0] == 'on'
        try:
            return execute_cmd(['blueutil', '-p', ('1' if on else '0')]).strip()
        except Exception as exception:
            error = exception.message if hasattr(exception, 'message') else str(exception)
            if "No such file or directory: 'blueutil'" in error:
                raise_error('`blueutil` is required:\nbrew install blueutil')
            else:
                return f"unhandled error: {error}"

    def parse_argv(self, argv: List[str]) -> List[str]:
        if len(argv) == 0:
            raise_error('No option provided', usage=self.usage)
        if argv[0] not in ('on', 'off'):
            raise_error(f"Unsupported option provided: {argv[0]}", usage=self.usage)
        return argv

    def usage(self) -> None:
        print_coloured('Usage:\n', 'white', 'bold')
        print_coloured('$ ./bluetooth.py <on/off>\n', 'white')


if __name__ == '__main__':
    result = Bluetooth(sys.argv[1:]).execute()
    if result != '':
        raise_error(f"Something went wrong; stdout: {result}")
