"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from slither.analyses.data_dependency.data_dependency import is_dependent
from slither.core.cfg.node import Node
from slither.core.solidity_types.elementary_type import Uint, Int
from slither.core.variables import StateVariable, Variable
from slither.core.variables.local_variable import LocalVariable
from slither.detectors.abstract_detector import DetectorClassification, DETECTOR_INFO
from slither.slithir.operations import Operation, Binary, BinaryType
from slither.slithir.variables import TemporaryVariable

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
    AbstractVariableInNodes,
)
from sother.detectors.detector_settings import DetectorSettings


class VariableZeroValidation(AbstractVariableInNodes):
    checking_variable_types = Uint + Int

    @classmethod
    def is_variable_checked_instance(cls, var: Variable, ir: Operation) -> bool:
        if str(var.type) not in cls.checking_variable_types:
            return False
        if (
            ir.node.contains_if()
            and isinstance(ir, Binary)
            and ir.type == BinaryType.EQUAL
        ) or (
            ir.node.contains_require_or_assert()
            and isinstance(ir, Binary)
            and ir.type
            in [
                BinaryType.LESS,
                BinaryType.GREATER,
                BinaryType.LESS_EQUAL,
                BinaryType.GREATER_EQUAL,
                BinaryType.NOT_EQUAL,
            ]
        ):
            if is_dependent(var, ir.variable_left, ir.node) or is_dependent(
                var, ir.variable_left, ir.node
            ):
                return True
        return False


class DivisionByZero(AbstractDetectHasInstance):
    ARGUMENT = "division-by-zero"
    HELP = "Division by zero not prevented"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Division by zero not prevented"

    WIKI_DESCRIPTION = """
In Solidity, transactions are reverted with the "division by zero" error
message when a division by zero is attempted.
Although divisions by zero will result in reversions, 
they will not have error messages, 
making failed transaction more difficult to debug by users.

Consider actively preventing divisions by zero with appropriate `revert` statements that 
have informative and user-friendly error messages.
"""

    WIKI_RECOMMENDATION = """
It is recommended to add a sanity check to control whether the borrowed
amount is zero or not.
"""
    WIKI_EXPLOIT_SCENARIO = " "

    @classmethod
    def _is_division_by_var(cls, ir: Operation) -> bool:
        if (
            isinstance(ir, Binary)
            and ir.type == BinaryType.DIVISION
            and isinstance(
                ir.variable_right, (StateVariable, LocalVariable, TemporaryVariable)
            )
        ):
            # except denominator is `Constant`
            if (
                isinstance(ir.variable_right, StateVariable)
                and ir.variable_right.is_constant
            ):
                return False

            # todo variable contains `*+1` statement
            if not VariableZeroValidation.is_variable_in_nodes(
                ir.variable_right,
                ir.node.fathers,
                [],
                VariableZeroValidation.TraverseType.FATHERS,
            ):
                return True

        return False

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        if cls._is_division_by_var(ir):
            return True
        return False

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            node,
            " possible divisions by `0` can be performed.",
            "\n",
        ]


if __name__ == "__main__":
    unittest.main()
