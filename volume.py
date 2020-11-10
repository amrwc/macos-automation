#!/usr/bin/env python3

"""
# Volume

A utility for changing the sound volume from command-line.

## Setup

Create a symlink to the script.

```console
ln -s "$(pwd)/volume.py" /usr/local/bin/volume
```

## Usage

Use a number between 0 and 7 to represent the volume level. The level is of a `float` type, so it can also have a
decimal place.

```console
volume <number>
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


class Volume(Automation):

    def __init__(self, argv: List[str] = []):
        self.argv = self.parse_argv(argv)

    def execute(self) -> str:
        log(f"Changing volume to {self.volume}")
        apple_script = self.build_apple_script(self.volume)
        return execute_cmd(['osascript', '-e', apple_script]).strip()

    def parse_argv(self, argv: List[str]) -> List[str]:
        if len(argv) == 0:
            raise_error('No option provided', usage=self.usage)
        volume = 1.0
        try:
            volume = float(argv[0])
        except ValueError:
            raise_error(f"Unsupported option provided: {argv[0]}", usage=self.usage)
        # Values beyond `7.0` seem to do nothing more than maxing out the volume
        if volume > 7.0:
            volume = 7.0
        elif volume < 0.0:
            volume = 0.0
        self.volume = volume
        return argv

    def usage(self) -> None:
        print_coloured('Usage:\n', 'white', 'bold')
        print_coloured('$ ./volume.py <number>\n', 'white')

    def build_apple_script(self, volume: float) -> str:
        """Builds an AppleScript snippet that changes the volume level.

        Args:
            volume (float): New volume level.

        Returns:
            AppleScript (osascript) snippet.
        """
        return f"set Volume {str(volume)}"


if __name__ == '__main__':
    Volume(sys.argv[1:]).execute()
