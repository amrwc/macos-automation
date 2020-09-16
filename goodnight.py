#!/usr/bin/env python3


"""
# Good Night

A utility for performing some of the common shutting down operations from
command-line in combination.

## Setup

Create a symlink to the script.

```console
ln -s "$(pwd)/goodnight.py" /usr/local/bin/goodnight
```

## Usage

```console
./goodnight.py
goodnight
```

@author: amrwc
"""

from typing import List

from abstract_automation import Automation
from bluetooth import Bluetooth
from sleep import Sleep
from wifi import Wifi
from utils import (
    log,
    print_coloured,
)


class Goodnight(Automation):

    def execute(self) -> str:
        log('Good night!')
        automations: List[Automation] = [
            Bluetooth(['off']),
            Sleep(),
            Wifi(['off']),
        ]
        for automation in automations:
            automation.execute()
        return ''

    def parse_argv(self, argv: List[str] = []) -> List[str]:
        return []

    def usage(self) -> None:
        print_coloured('Usage:\n', 'white', 'bold')
        print_coloured('$ ./goodnight.py\n', 'white')


if __name__ == '__main__':
    Goodnight().execute()