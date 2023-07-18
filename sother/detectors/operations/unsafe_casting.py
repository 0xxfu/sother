"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.declarations import FunctionContract
from slither.core.expressions import (
    AssignmentOperation,
    BinaryOperation,
    BinaryOperationType,
    Identifier,
    TypeConversion,
)
from slither.core.expressions.expression import Expression
from slither.core.solidity_types.elementary_type import Uint, Int
from slither.core.variables import Variable
from slither.core.variables.local_variable import LocalVariable
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.slithir.operations import (
    Assignment,
    TypeConversion as IrTypeConversion,
    Binary,
    BinaryType,
    Operation,
)
from slither.utils.output import Output

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings


class UnsafeDowncast(AbstractDetector):
    ARGUMENT = "unsafe-downcast"
    HELP = "Unsafe downcasting arithmetic operation"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Unsafe downcasting arithmetic operation"
    WIKI_DESCRIPTION = """
Downcasting from uint256/int256 in Solidity does not revert on overflow.
When a type is downcast to a smaller type, the higher order bits are truncated, 
effectively applying a modulo to the original value. 
Without any other checks, this wrapping will lead to unexpected behavior and bugs.
"""

    WIKI_RECOMMENDATION = """
Just use `uint256/int256`, or use [OpenZeppelin SafeCast lib](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/math/SafeCast.sol#).
"""
    WIKI_EXPLOIT_SCENARIO = " "

    def _detect(self) -> list[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for function in contract.functions:
                # if function.name not in ["toInt8"]:
                #     continue
                result_nodes: set[Node] = self._detect_unsafe_downcast(function)
                for node in result_nodes:
                    res = self.generate_result(
                        [
                            node,
                            " should use `uint256/int256` or `OpenZeppelin SafeCast lib`.",
                        ]
                    )
                    results.append(res)
        return results

    @classmethod
    def _is_type_max_expression(cls, expression: Expression) -> bool:
        # type()(uint128).max
        if "type()" in str(expression) and ".max" in str(expression):
            return True
        return False

    @classmethod
    def _detect_var_compare_max(cls, function: FunctionContract) -> set[Variable]:
        result_vars: set[Variable] = set()
        for node in function.nodes:
            node_exp = node.expression
            if (
                node.contains_if()
                and isinstance(node_exp, BinaryOperation)
                and node_exp.type
                in [
                    BinaryOperationType.LESS,
                    BinaryOperationType.GREATER,
                    BinaryOperationType.LESS_EQUAL,
                    BinaryOperationType.GREATER_EQUAL,
                ]
            ):
                if cls._is_type_max_expression(node_exp.expression_right):
                    if isinstance(node_exp.expression_left, Identifier) and isinstance(
                        node_exp.expression_left.value, Variable
                    ):
                        result_vars.add(node_exp.expression_left.value)
                elif cls._is_type_max_expression(node_exp.expression_left):
                    if isinstance(node_exp.expression_right, Identifier) and isinstance(
                        node_exp.expression_right.value, Variable
                    ):
                        result_vars.add(node_exp.expression_right.value)
        return result_vars

    @classmethod
    def _detect_compare(
        cls, function: FunctionContract
    ) -> set[tuple[Variable, Variable]]:
        """
        detect "if (downcasted != value)" in funciton
        and packing compare variable into tuple
        """
        result_variables: set[tuple[Variable, Variable]] = set()
        for node in function.nodes:
            for ir in node.irs:
                if isinstance(ir, Binary) and ir.type == BinaryType.NOT_EQUAL:
                    result_variables.add((ir.variable_left, ir.variable_right))
                    result_variables.add((ir.variable_right, ir.variable_left))
        return result_variables

    @classmethod
    def _detect_unsafe_downcast(cls, function: FunctionContract) -> set[Node]:
        result_nodes: set[Node] = set()
        all_int = Uint + Int

        var_has_compare_max: set[Variable] = cls._detect_var_compare_max(function)
        compare_variables: set[tuple[Variable, Variable]] = cls._detect_compare(
            function
        )
        for node in function.nodes:
            for ir in node.irs:
                ir_exp = ir.expression
                if (
                    isinstance(ir, IrTypeConversion)
                    and all(
                        [
                            str(ir.lvalue.type) in all_int,
                            str(ir.variable.type) in all_int,
                        ]
                    )
                    and ir.variable.type.size > ir.lvalue.type.size
                    and ir.variable not in var_has_compare_max
                ):
                    result_nodes.add(node)
                elif (
                    isinstance(ir, Assignment)
                    and isinstance(ir_exp, AssignmentOperation)
                    and isinstance(ir_exp.expression_right, TypeConversion)
                    and isinstance(ir_exp.expression_right.expression, Identifier)
                    and isinstance(ir_exp.expression_left, Identifier)
                ):
                    # "if (downcasted != value)" statement in compare
                    # remove node
                    if (
                        ir_exp.expression_left.value,
                        ir_exp.expression_right.expression.value,
                    ) in compare_variables:
                        result_nodes.remove(node)
        return result_nodes


class UnsafeDoubleCast(AbstractDetectHasInstance):
    ARGUMENT = "unsafe-double-cast"
    HELP = "Double type casts create complexity within the code"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Double type casts create complexity within the code"

    WIKI_DESCRIPTION = """
Double type casting should be avoided in Solidity contracts to prevent unintended 
consequences and ensure accurate data representation. 
Performing multiple type casts in succession can lead to unexpected truncation, 
rounding errors, or loss of precision, potentially compromising the contract's 
functionality and reliability. Furthermore, double type casting can make the code 
less readable and harder to maintain, increasing the likelihood of errors and 
misunderstandings during development and debugging. To ensure precise and consistent 
data handling, developers should use appropriate data types and avoid unnecessary 
or excessive type casting, promoting a more robust and dependable contract execution.
"""
    WIKI_EXPLOIT_SCENARIO = """ """

    WIKI_RECOMMENDATION = """
Consider using single casting instead of double casting.
"""

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        if isinstance(ir, IrTypeConversion):
            all_int = Uint + Int
            cast_count = 0
            for node_ir in ir.node.irs:
                if isinstance(node_ir, IrTypeConversion) and all(
                    [
                        str(ir.lvalue.type) in all_int,
                        str(ir.variable.type) in all_int,
                    ]
                ):
                    cast_count += 1

            if cast_count >= 2:
                return True

        return False

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            node,
            " should use single casting instead of double casting.",
            "\n",
        ]


if __name__ == "__main__":
    unittest.main()
