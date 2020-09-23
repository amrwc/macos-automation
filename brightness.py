#!/usr/bin/env python3

"""
# Brightness

A utility for changing the screen brightness from command-line.

## Setup

1. Install `brightness` via Homebrew or from source – according to some comments in the GitHub issues, building from
   source may fix some issues with external monitors.

   ```console
   brew install brightness
   ```

   ```console
   git clone https://github.com/nriley/brightness.git
   cd brightness
   make
   sudo make install
   ```

1. Create a symlink to the script. Note that since this script depends on `brightness` from Homebrew, the symlink
   cannot have the same name.

   ```console
   ln -s "$(pwd)/brightness.py" /usr/local/bin/bright
   ```

## Usage

Use a decimal between 0 and 1 to represent the brightness percentage.

```console
./brightness.py <decimal>
bright <decimal>
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


class Brightness(Automation):

    def __init__(self, argv: List[str] = []):
        self.argv = self.parse_argv(argv)

    def execute(self) -> str:
        log(f"Changing brightness to {self.brightness}")
        return execute_cmd(['brightness', str(self.brightness)])

    def parse_argv(self, argv: List[str]) -> List[str]:
        if len(argv) == 0:
            raise_error('No option provided', usage=self.usage)
        brightness: float = 0.5
        try:
            brightness = float(argv[0])
        except ValueError:
            raise_error(f"Unsupported option provided: {argv[0]}", usage=self.usage)
        if brightness > 1.0:
            brightness = 1.0
        elif brightness < 0.0:
            brightness = 0.0
        self.brightness = brightness
        return argv

    def usage(self) -> None:
        print_coloured('Usage:\n', 'white', 'bold')
        print_coloured('$ ./brightness.py <decimal>\n', 'white')


if __name__ == '__main__':
    Brightness(sys.argv[1:]).execute()
