#!/usr/bin/env python3

"""
# Setup

Script for setting up symlinks to the macOS automations in this directory.

@author: amrwc
"""

import os

from utils import log


BIN_PATH = '/usr/local/bin'
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))


class Automation():
    def __init__(self, script_name: str, symlink_name: str):
        self.script_name = script_name
        self.symlink_name = symlink_name


AUTOMATIONS = [
    Automation('appearance', 'appearance'),
    Automation('bluetooth', 'bluetooth'),
    Automation('brightness', 'bright'),
    Automation('goodnight', 'goodnight'),
    Automation('hello', 'hello'),
    Automation('sleep', 'night'),
    Automation('tunnelblick', 'tunnelblick'),
    Automation('volume', 'volume'),
    Automation('wifi', 'wifi'),
]


def main() -> None:
    """The script's main entry point"""
    for automation in AUTOMATIONS:
        source = f"{SCRIPT_PATH}/{automation.script_name}.py"
        destination = f"{BIN_PATH}/{automation.symlink_name}"
        if os.path.islink(destination):
            log(f"'{destination}' symlink already exists. Skipping")
            continue
        log(f"Creating symlink to '{source}'. It'll be available as '{automation.symlink_name}'")
        os.symlink(source, destination, target_is_directory=False)


if __name__ == '__main__':
    main()
