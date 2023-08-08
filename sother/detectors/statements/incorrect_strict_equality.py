"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-08
"""
import unittest

from slither.detectors.statements.incorrect_strict_equality import (
    IncorrectStrictEquality as SlitherIncorrectStrictEquality,
)
from slither.slithir.operations import Operation, Binary, BinaryType
from slither.slithir.variables import Constant


class IncorrectStrictEquality(SlitherIncorrectStrictEquality):
    @staticmethod
    def is_direct_comparison(ir: Operation) -> bool:
        if isinstance(ir, Binary) and ir.type == BinaryType.EQUAL:
            # except equal `0` statement: `variable == 0;`
            if any(
                [
                    isinstance(ir.variable_right, Constant)
                    and ir.variable_right.value == 0,
                    isinstance(ir.variable_left, Constant)
                    and ir.variable_left.value == 0,
                ]
            ):
                return False
            return True
        return False


if __name__ == "__main__":
    unittest.main()
