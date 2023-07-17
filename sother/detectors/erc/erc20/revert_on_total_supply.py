"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.analyses.data_dependency.data_dependency import is_dependent
from slither.core.cfg.node import Node
from slither.core.declarations import Function
from slither.core.expressions import (
    BinaryOperation,
    BinaryOperationType,
    CallExpression,
    AssignmentOperation,
)
from slither.core.variables import Variable
from slither.detectors.abstract_detector import DetectorClassification, DETECTOR_INFO
from slither.slithir.operations import (
    Operation,
    HighLevelCall,
    InternalCall,
    Binary,
    BinaryType,
)

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
    AbstractVariableInNodes,
)
from sother.detectors.detector_settings import DetectorSettings


class SupplyChecked(AbstractVariableInNodes):
    @classmethod
    def is_variable_checked_instance(cls, var: Variable, ir: Operation) -> bool:
        if (
            isinstance(ir, HighLevelCall)
            and isinstance(ir.function, Function)
            and ir.function.solidity_signature
            in [
                "totalSupply()",
            ]
            and (ir.node.contains_if() or ir.node.contains_require_or_assert())
        ):
            return True
        else:
            if (
                var is not None
                and isinstance(ir, Binary)
                and ir.type
                in [
                    BinaryType.LESS,
                    BinaryType.LESS_EQUAL,
                    BinaryType.GREATER,
                    BinaryType.GREATER_EQUAL,
                    BinaryType.EQUAL,
                    BinaryType.NOT_EQUAL,
                ]
            ):
                for var_read in ir.read:
                    if is_dependent(var_read, var, ir.node):
                        return True

        return False


class VariableInDivisionRight(AbstractVariableInNodes):
    @classmethod
    def is_variable_checked_instance(cls, var: Variable, ir: Operation) -> bool:
        if isinstance(ir, Binary) and ir.type == BinaryType.DIVISION:
            if is_dependent(var, ir.variable_right, ir.node):
                return True
        return False


class RevertOnTotalSupply(AbstractDetectHasInstance):
    ARGUMENT = "revert-on-total-supply"
    HELP = "Calls will revert when `totalSupply()` returns zero"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Calls will revert when `totalSupply()` returns zero"

    WIKI_DESCRIPTION = """
`totalSupply()` being zero will result in a division by zero, 
causing the transaction to fail. 
The function should instead special-case this scenario, and avoid reverting.
"""

    WIKI_RECOMMENDATION = """
Checking if `totalSupply()` greater than zero before division. 
"""
    WIKI_EXPLOIT_SCENARIO = " "

    @classmethod
    def _is_supply_in_division_and_checked(cls, ir: Operation) -> bool:
        if (
            isinstance(ir, HighLevelCall)
            and isinstance(ir.function, Function)
            and ir.function.solidity_signature
            in [
                "totalSupply()",
            ]
        ):
            node_exp = ir.node.expression
            if (
                isinstance(node_exp, BinaryOperation)
                and node_exp.type == BinaryOperationType.DIVISION
                and isinstance(node_exp.expression_right, CallExpression)
                and "totalSupply()" in str(node_exp.expression_right)
            ):
                if not SupplyChecked.is_variable_in_nodes(None, ir.node.function.nodes):
                    return True
            elif isinstance(node_exp, AssignmentOperation):
                for var in ir.node.variables_written:
                    if VariableInDivisionRight.is_variable_in_nodes(var, ir.node.sons):
                        if not SupplyChecked.is_variable_in_nodes(
                            var, ir.node.function.nodes
                        ):
                            return True

        return False

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        if cls._is_supply_in_division_and_checked(ir):
            return True
        return False

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            node,
            " should check if `totalSupply()` greater than zero before division.",
            "\n",
        ]


if __name__ == "__main__":
    unittest.main()
