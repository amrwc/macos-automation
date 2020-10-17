#!/usr/bin/env python3

"""
# Appearance

A utility for changing the system's appearance from command-line.

Supported commands:

- dark -- sets apprearance to dark mode.
- light -- sets appearance to light mode.
- toggle -- toggles appearance to the opposite state.

## Setup

Create a symlink to the script.

```console
ln -s "$(pwd)/appearance.py" /usr/local/bin/appearance
```

## Usage

```console
appearance <dark/light/toggle>
```

@author: amrwc
"""

import sys
from typing import List, Tuple

from abstract_automation import Automation
from utils import (
    execute_cmd,
    log,
    print_coloured,
    raise_error,
)


class Appearance(Automation):

    def __init__(self, argv: List[str] = []):
        self.argv = self.parse_argv(argv)

    def execute(self) -> str:
        current_mode = self.get_current_mode()
        is_currently_dark = current_mode == 'dark'
        if self.toggle:
            log(f"Changing system's appearance from '{current_mode}' to '{'light' if is_currently_dark else 'dark'}'")
            return self.tell_appearance_preferences(('set dark mode to not dark mode',))
        else:
            if current_mode == self.mode:
                log(f"Not changing system's appearance; it's already set to '{self.mode}'")
                return ''
            else:
                log(f"Changing system's appearance to '{self.mode}'")
                return self.tell_appearance_preferences(
                    (f"set dark mode to {'false' if is_currently_dark else 'true'}",))

    def parse_argv(self, argv: List[str]) -> List[str]:
        if len(argv) == 0:
            raise_error('No option provided', usage=self.usage)
        if argv[0] not in ('dark', 'light', 'toggle'):
            raise_error(f"Unsupported option provided: {argv[0]}", usage=self.usage)
        if argv[0] == 'toggle':
            self.mode = None
            self.toggle = True
        else:
            self.mode = argv[0]
            self.toggle = False
        return []

    def usage(self) -> None:
        print_coloured('Usage:\n', 'white', 'bold')
        print_coloured('$ ./appearance.py <dark/light/toggle>\n', 'white')

    def get_current_mode(self) -> str:
        apple_script = ('if dark mode then',
                        '    return "dark"',
                        'else',
                        '    return "light"',
                        'end if')
        return self.tell_appearance_preferences(apple_script)

    def tell_appearance_preferences(self, apple_script: Tuple[str]) -> str:
        cmd = '\n'.join(
            ('tell application "System Events"', 'tell appearance preferences')
            + apple_script
            + ('end tell', 'end tell')
        )
        return execute_cmd(['osascript', '-e', cmd]).strip()


if __name__ == '__main__':
    result = Appearance(sys.argv[1:]).execute()
    if result != '':
        raise_error(f"Something went wrong; stdout: {result}")
