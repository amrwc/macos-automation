from abc import ABC, abstractmethod
from typing import List


class Automation(ABC):

    @abstractmethod
    def execute(self) -> str:
        """
        Entry point of the automation script.
        @return: stdout
        """
        pass

    @abstractmethod
    def parse_argv(self, argv: List[str]) -> List[str]:
        """
        Parses and verifies the command-line arguments and returns them with the script name removed.
        @return: command-line arguments
        """
        pass

    @abstractmethod
    def usage(self) -> None:
        """Prints usage instructions."""
        pass
