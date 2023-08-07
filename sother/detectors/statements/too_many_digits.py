"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-08
"""
import re
import unittest

from slither.core.cfg.node import Node
from slither.core.declarations import FunctionContract
from slither.detectors.statements.too_many_digits import (
    TooManyDigits as SlitherTooManyDigits,
    is_hex_address,
)
from slither.slithir.variables import Constant


class TooManyDigits(SlitherTooManyDigits):
    @staticmethod
    def _detect_too_many_digits(f: FunctionContract) -> list[Node]:
        ret = []
        for node in f.nodes:
            # each node contains a list of IR instruction
            for ir in node.irs:
                # iterate over all the variables read by the IR
                for read in ir.read:
                    # if the variable is a constant
                    if isinstance(read, Constant):
                        # exclude creationCode statement `type(Contract).creationCode`
                        if re.compile(r"type\(\)\(.*\)\.creationCode").findall(
                            str(ir.expression)
                        ):
                            continue
                        # read.value can return an int or a str. Convert it to str
                        value_as_str = read.original_value
                        if "00000" in value_as_str and not is_hex_address(value_as_str):
                            # Info to be printed
                            ret.append(node)
        return ret


if __name__ == "__main__":
    unittest.main()
