"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.variables import StateVariable
from slither.core.variables.local_variable import LocalVariable
from slither.detectors.abstract_detector import DetectorClassification, DETECTOR_INFO
from slither.slithir.operations import Operation, Binary, BinaryType
from slither.slithir.variables import TemporaryVariable

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings

# todo impl
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
            return True
        return False

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        if ir.node.function.name != "bad0":
            return False
        if cls._is_division_by_var(ir):
            logger.debug(f"ir: {ir.expression} type: {type(ir)}")
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
