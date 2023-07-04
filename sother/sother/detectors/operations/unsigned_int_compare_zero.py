"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest
from typing import List, Optional

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.declarations import FunctionContract
from slither.core.expressions import (
    BinaryOperation,
    BinaryOperationType,
    CallExpression,
    Identifier,
    Literal,
)
from slither.core.expressions.expression import Expression
from slither.core.solidity_types import ElementaryType
from slither.core.solidity_types.elementary_type import Uint
from slither.core.variables import Variable
from slither.core.variables.local_variable import LocalVariable
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class UnsignedIntCompareZero(AbstractDetector):
    ARGUMENT = "unsigned-int-compare-zero"
    HELP = "`!= 0` is less gas than `> 0` for unsigned integers"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "`++i` costs less gas than `i++`, especially when it's used in for-loops (`--i/i--` too)"

    WIKI_DESCRIPTION = """
`!= 0` costs less gas compared to `> 0` for unsigned integers in require statements 
with the optimizer enabled (6 gas)

While it may seem that `> 0` is cheaper than `!=`, this is only true without the 
optimizer enabled and outside a require statement. 
If you enable the optimizer at 10k and you’re in a `require` statement, 
this will save gas.

"""

    WIKI_RECOMMENDATION = """
Use `!= 0` instead of `> 0` for unsigned integer comparison.
"""

    @classmethod
    def _is_uint_compare_zero(cls, operation: BinaryOperation) -> bool:
        if isinstance(operation, BinaryOperation):
            op_left = operation.expression_left
            op_right = operation.expression_right
            variable: Optional[Variable] = None
            literal: Optional[Literal] = None
            if (
                isinstance(op_left, Identifier)
                and isinstance(op_left.value, Variable)
                and isinstance(op_right, Literal)
            ):
                variable = op_left.value
                literal = op_right
            elif (
                isinstance(op_left, Literal)
                and isinstance(op_right, Identifier)
                and isinstance(op_right.value, Variable)
            ):
                variable = op_right.value
                literal = op_left

            if (
                variable
                and literal
                and variable.type.type in Uint
                and literal.value == "0"
            ):
                return True
        return False

    @classmethod
    def _detect_compare_zero(cls, function: FunctionContract) -> set[Node]:
        result_nodes: [Node] = set()

        for node in function.nodes:
            # logger.debug(f"exp: {node.expression} type: {type(node.expression)}")

            if (
                node.contains_if()
                and isinstance(node.expression, BinaryOperation)
                and node.expression.type == BinaryOperationType.GREATER
            ):  # if (x>0)
                if cls._is_uint_compare_zero(node.expression):
                    result_nodes.add(node)
            elif any(
                c.name in ["require(bool)", "require(bool,string)"]
                for c in node.internal_calls
            ):  # require (x>0)
                node_exp = node.expression
                if not isinstance(node_exp, CallExpression):
                    continue

                for argument in node_exp.arguments:
                    if (
                        isinstance(argument, BinaryOperation)
                        and (argument.type == BinaryOperationType.GREATER)
                        and cls._is_uint_compare_zero(argument)
                    ):
                        result_nodes.add(node)

        return result_nodes

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for function in contract.functions:
                result_nodes: set[Node] = self._detect_compare_zero(function)
                for node in result_nodes:
                    res = self.generate_result(
                        [
                            node,
                            " should use `!= 0` instead of `> 0` for unsigned integer comparison.\n",
                        ]
                    )
                    results.append(res)
        return results


if __name__ == "__main__":
    unittest.main()
