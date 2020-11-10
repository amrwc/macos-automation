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

```console
wifi <on/off>
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


class Wifi(Automation):

    def __init__(self, argv: List[str] = []):
        self.argv = self.parse_argv(argv)

    def execute(self) -> str:
        return self.set_wifi(self.argv[0] == 'on')

    def parse_argv(self, argv: List[str]) -> List[str]:
        if len(argv) == 0:
            raise_error('No option provided', usage=self.usage)
        if argv[0] not in ('on', 'off'):
            raise_error(f"Unsupported option provided: {argv[0]}", usage=self.usage)
        return argv

    def usage(self) -> None:
        print_coloured('Usage:\n', 'white', 'bold')
        print_coloured('$ ./wifi.py <on/off>\n', 'white')

    def set_wifi(self, on: bool) -> str:
        """Turns Wi-Fi to the given state.

        Args:
            on (bool): Whether to turn Wi-Fi on.

        Returns:
            Stdout of the command execution.
        """
        power = 'on' if on else 'off'
        log(f"Turning Wi-Fi {power}")
        # 'Hardware Port: Wi-Fi\nDevice: en0 ...'
        hardware_ports = execute_cmd(['networksetup', '-listallhardwareports']).strip()
        # ['Hardware Port: Wi-Fi', 'Device: en0']
        hardware_ports_lines = hardware_ports.splitlines()
        device_name = ''
        for i, line in enumerate(hardware_ports_lines):
            if 'Wi-Fi' in line:  # 'Hardware Port: Wi-Fi'
                device_name_line = hardware_ports_lines[i + 1]  # 'Device: en0'
                device_name = device_name_line.split()[1]  # 'en0'
                break
        return execute_cmd(['networksetup', '-setairportpower', device_name, power]).strip()


if __name__ == '__main__':
    result = Wifi(sys.argv[1:]).execute()
    if result != '':
        raise_error(f"Something went wrong; stdout: {result}")
