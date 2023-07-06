"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List, Tuple, Optional

from loguru import logger
from slither.core.cfg.node import NodeType, Node
from slither.core.declarations import Contract, Function, FunctionContract
from slither.core.expressions import BinaryOperation, CallExpression
from slither.core.solidity_types import ArrayType
from slither.core.variables import Variable
from slither.core.variables.local_variable import LocalVariable
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.slithir.operations import Binary, BinaryType, Length
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class UncheckedArrayLength(AbstractDetector):
    ARGUMENT = "unchecked-array-length"
    HELP = "Missing array length check when inputting multiple arrays"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Missing array length equality checks may lead to incorrect or undefined behavior"
    WIKI_DESCRIPTION = """
If the length of the arrays are not required to be of the same length, user operations may not be fully executed due to a mismatch in the number of items iterated over, versus the number of items provided in the second array
"""

    WIKI_RECOMMENDATION = """
Check if the lengths of the array parameters are equal before use.
"""
    WIKI_EXPLOIT_SCENARIO = " "

    def _detect(self) -> List[Output]:
        """
        1. get input array list
        2. detect require/if/asset statements
        3. return function and input variables
        """
        results = []
        for c in self.compilation_unit.contracts:
            for func in c.functions_declared:
                if not func.is_implemented:
                    continue
                # if func.name != "goodWithRevert":
                #     continue
                variables: set[Variable] = self._detect_unchecked_array_length(func)
                if not variables:
                    continue
                result = [
                    "Missing check lengths of parameters below in function ",
                    func,
                    ":\n",
                ]
                for var in variables:
                    result += ["\t- ", var, "\n"]
                res = self.generate_result(result)
                results.append(res)
        return results

    @classmethod
    def _is_checked_array_length(
        cls, variables: set[LocalVariable], node: Node
    ) -> bool:
        # check irs in node has array length check
        array_length: set[LocalVariable] = set()
        for ir in node.irs:
            if isinstance(ir, Length):
                for item in ir.read:
                    if item in variables:
                        array_length.add(item)
            if not isinstance(ir, Binary):
                continue
            if ir.type == BinaryType.EQUAL or ir.type == BinaryType.NOT_EQUAL:
                if len(array_length) == len(variables):
                    return True
        return False

    @classmethod
    def _detect_unchecked_array_length(
        cls, function: FunctionContract
    ) -> Optional[set[Variable]]:
        arr_variables: set[LocalVariable] = set()
        for param in function.parameters:
            if isinstance(param.type, ArrayType):
                arr_variables.add(param)

        if len(arr_variables) <= 1:
            return

        # detect if/require/asset statements
        for node in function.nodes:
            # check node is `if` BinaryOperation node or `require`/`assert` CallExpression node
            if (
                isinstance(node.expression, BinaryOperation)
                and node.type == NodeType.IF
            ):
                if cls._is_checked_array_length(arr_variables, node):
                    return None
            elif isinstance(node.expression, CallExpression) and any(
                c.name == "assert(bool)" or c.name == "require(bool,string)"
                for c in node.internal_calls
            ):
                if cls._is_checked_array_length(arr_variables, node):
                    return None
        return arr_variables


if __name__ == "__main__":
    unittest.main()
