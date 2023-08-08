"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.expressions import BinaryOperation, Literal, BinaryOperationType
from slither.core.solidity_types.elementary_type import Uint
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings
from sother.utils.gas_utils import GasUtils


class DivideByConstant(AbstractDetector):
    ARGUMENT = "divide-by-constant"
    HELP = "Using `x >> constant(uint)` with the right shift operator is a more gas-efficient"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Using `x >> constant(uint)` with the right shift operator is a more gas-efficient"
    WIKI_DESCRIPTION = """
`<x> / 2` is the same as `<x> >> 1`. While the compiler uses the `SHR` opcode to accomplish both, 
the version that uses division incurs an overhead of [**20 gas**](https://gist.github.com/0xxfu/84e3727f28e01f9b628836d5bf55d0cc) 
due to `JUMP`s to and from a compiler utility function that introduces checks which can 
be avoided by using `unchecked {}` around the division by two

"""

    WIKI_RECOMMENDATION = """
Using bit shifting (`>>` operator) replace division divided by constant.
"""

    def _detect(self) -> List[Output]:
        results = []
        divide_expressions: list[Node] = []
        uint_list = Uint
        for function in GasUtils.get_available_functions(self.compilation_unit):
            for node in function.nodes:
                for ir in node.irs:
                    ir_exp = ir.expression
                    # expression is `/` operator
                    if (
                        isinstance(ir_exp, BinaryOperation)
                        and ir_exp.type == BinaryOperationType.DIVISION
                    ):
                        exp_right = ir_exp.expression_right
                        # division divided by constant(uint)
                        if (
                            isinstance(exp_right, Literal)
                            and str(exp_right.type) in uint_list
                        ):
                            logger.debug(f"divided by constant: {ir_exp}")
                            divide_expressions.append(node)

        for exp in divide_expressions:
            res = self.generate_result(
                [
                    exp,
                    " should use right shift `>>` operator to save gas.\n",
                ]
            )
            results.append(res)
        return results


class MulPowerTwo(AbstractDetector):
    ARGUMENT = "mul-power-two"
    HELP = "Multiplications of powers of 2 can be replaced by a left shift operation to save gas"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki
    WIKI_TITLE = "Multiplications of powers of 2 can be replaced by a left shift operation to save gas"

    WIKI_DESCRIPTION = """
`1 << x` is the same as `2**x`. 
A multiplication by any number x being a power of 2 can be calculated by shifting to the left. 
While the `EXP` opcode uses [`gas_cost = 10 + 50 * byte_len_exponent`](https://github.com/wolflo/evm-opcodes/blob/main/gas.md#a1-exp), 
the `SHL` opcode only uses 3 gas.

"""

    WIKI_RECOMMENDATION = """
Using bit shifting (`<<` operator) replace multiplications of powers of 2 `(2**x)`.
"""

    def _detect(self) -> List[Output]:
        results = []
        powers_of_2: list[Node] = []
        uint_list = Uint
        for function in GasUtils.get_available_functions(self.compilation_unit):
            for node in function.nodes:
                for ir in node.irs:
                    ir_exp = ir.expression
                    # expression is `**` operator
                    if (
                        isinstance(ir_exp, BinaryOperation)
                        and ir_exp.type == BinaryOperationType.POWER
                    ):
                        exp_left = ir_exp.expression_left
                        # multiplications of powers of 2
                        # `2**x`
                        if (
                            isinstance(exp_left, Literal)
                            and str(exp_left.type) in uint_list
                            and exp_left.value == "2"
                        ):
                            powers_of_2.append(node)

        for exp in powers_of_2:
            res = self.generate_result(
                [
                    exp,
                    " should use bit shifting (`<<` operator) to save gas.\n",
                ]
            )
            results.append(res)
        return results


if __name__ == "__main__":
    unittest.main()
