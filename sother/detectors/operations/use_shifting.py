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
from slither.core.expressions.expression import Expression
from slither.core.solidity_types.elementary_type import Int, Uint
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings
from sother.utils.gas_utils import GasUtils


# todo detect except function
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
                for ir in node.all_slithir_operations():
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


if __name__ == "__main__":
    unittest.main()
