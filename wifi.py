#!/usr/bin/env python3

"""
# Wi-Fi

A utility for turning Wi-Fi on/off from command-line.

## Setup

Create a symlink to the script:

```console
ln -s "$(pwd)/wifi.py" /usr/local/bin/wifi
```

## Usage

```
wifi <on/off>
```

@author: amrwc
"""

import sys
from typing import List
from utils import (
    execute_cmd,
    log,
    print_coloured,
    raise_error,
)


def main() -> None:
    """
    The application's entry point.
    """
    argv: List[str] = sys.argv[1:]
    if len(argv) == 0:  # Strip the script's name from argv
        raise_error('No option provided', usage=usage)
    if argv[0] not in ('on', 'off'):
        raise_error(f"Unsupported option provided: {argv[0]}", usage=usage)
    set_wifi(argv[0] == 'on')


def set_wifi(on: bool) -> None:
    """
    Turns Wi-Fi to the given state.
    @param on: whether to turn Wi-Fi on
    """
    power: str = 'on' if on else 'off'
    log(f"Turning Wi-Fi {power}")
    # '\nHardware Port: Wi-Fi\nDevice: en0\n ...'
    hardware_ports: str = execute_cmd(['networksetup', '-listallhardwareports'])
    # ['Hardware Port: Wi-Fi', 'Device: en0']
    hardware_ports_lines: List[str] = hardware_ports.splitlines()
    device_name: str = ''
    for i, line in enumerate(hardware_ports_lines):
        if 'Wi-Fi' in line:  # 'Hardware Port: Wi-Fi'
            device_name_line: str = hardware_ports_lines[i + 1]  # 'Device: en0'
            device_name = device_name_line.split()[1]  # 'en0'
            break
    execute_cmd(['networksetup', '-setairportpower', device_name, power])


def usage() -> None:
    """
    Prints usage instructions.
    """
    print_coloured('Usage:\n', 'white', 'bold')
    print_coloured('$ ./wifi.py <on/off>\n', 'white')


if __name__ == '__main__':
    main()
