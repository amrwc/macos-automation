#!/usr/bin/env python3


"""
# Hello

A utility for performing some of the common turning on operations from
command-line in combination.

## Setup

Create a symlink to the script.

```console
ln -s "$(pwd)/hello.py" /usr/local/bin/hello
```

## Usage

```console
hello
```

@author: amrwc
"""


from typing import List

from abstract_automation import Automation
from bluetooth import Bluetooth
from wifi import Wifi
from utils import (
    log,
    print_coloured,
)


class Hello(Automation):

    def execute(self) -> str:
        log('Hello!')
        automations = [
            Bluetooth(['on']),
            Wifi(['on']),
        ]
        for automation in automations:
            automation.execute()
        return ''

    def parse_argv(self, argv: List[str] = []) -> List[str]:
        return []

    def usage(self) -> None:
        print_coloured('Usage:\n', 'white', 'bold')
        print_coloured('$ ./hello.py\n', 'white')


if __name__ == '__main__':
    Hello().execute()
