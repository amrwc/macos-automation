#!/usr/bin/env python3

"""
# Sleep

A utility for putting the machine to sleep from command-line.

## Setup

Create a symlink to the script.

```console
ln -s "$(pwd)/sleep.py" /usr/local/bin/sleep
```

## Usage

```console
sleep
```

@author: amrwc
"""

from utils import (
    execute_cmd,
    log,
    raise_error,
)


def main() -> None:
    """
    The application's entry point.
    """
    log('Putting the machine to sleep')
    stdout: str = execute_cmd(['pmset', 'sleepnow'])
    if stdout != 'Sleeping now...\n':
        raise_error(f"Something went wrong; stdout: {stdout}")


if __name__ == '__main__':
    main()
