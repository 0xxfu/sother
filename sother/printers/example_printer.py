"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from slither.printers.abstract_printer import AbstractPrinter
from slither.utils import output


class ExamplePrinter(AbstractPrinter):
    WIKI = (
        "https://github.com/crytic/slither/wiki/Printer-documentation#constructor-calls"
    )
    ARGUMENT = "example-printer"
    HELP = "Print example"

    def output(self, filename: str) -> output.Output:
        print("example printer")
        return self.generate_output("example printer")


if __name__ == "__main__":
    unittest.main()
