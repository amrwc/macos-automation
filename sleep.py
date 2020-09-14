#!/usr/bin/env python3

"""
# Sleep

A utility for putting the machine to sleep from command-line.

## Setup

Create a symlink to the script. Remember that there's a built-in `sleep`
utility in the system that takes precedence. That's why it's necessary to
choose a different name.

```console
ln -s "$(pwd)/sleep.py" /usr/local/bin/night
```

## Usage

```console
./sleep.py
night
```

@author: amrwc
"""

from typing import List

from abstract_automation import Automation
from utils import (
    execute_cmd,
    log,
    print_coloured,
    raise_error,
)


class Sleep(Automation):

    def execute(self) -> str:
        log('Putting the machine to sleep')
        return execute_cmd(['pmset', 'sleepnow']).strip()

    def parse_argv(self, argv: List[str]) -> List[str]:
        return []

    def usage(self) -> None:
        print_coloured('Usage:\n', 'white', 'bold')
        print_coloured('$ ./sleep.py\n', 'white')


if __name__ == '__main__':
    result: str = Sleep().execute()
    if result != 'Sleeping now...':
        raise_error(f"Something went wrong; stdout: {result}")
