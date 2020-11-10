from abc import ABC, abstractmethod
from typing import List


class Automation(ABC):

    @abstractmethod
    def execute(self) -> str:
        """Entry point of the automation script.

        Returns:
            Standard output.
        """
        pass

    @abstractmethod
    def parse_argv(self, argv: List[str]) -> List[str]:
        """Parses and verifies the command-line arguments and returns them with the script name removed.

        Args:
            argv: Command-line arguments.

        Returns:
            Parsed arguments.
        """
        pass

    @abstractmethod
    def usage(self) -> None:
        """Prints usage instructions."""
        pass
