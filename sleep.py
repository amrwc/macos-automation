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
