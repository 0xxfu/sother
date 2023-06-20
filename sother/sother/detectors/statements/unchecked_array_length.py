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
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class UncheckedArrayLength(AbstractDetector):
    ARGUMENT = "unchecked-array-length"
    HELP = "Missing array length check when inputting multiple arrays"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Missing array length check when inputting multiple arrays"
    WIKI_DESCRIPTION = """
If the length of the arrays are not required to be of the same length, user operations may not be fully executed due to a mismatch in the number of items iterated over, versus the number of items provided in the second array
"""

    WIKI_RECOMMENDATION = """
At the beginning of the function, check if the length of the array is equal
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
                variables: list[Variable] = self._detect_unchecked_array_length(func)
                if not variables:
                    continue
                info: DETECTOR_INFO = ["if the array length of "]
                for variable in variables:
                    info.append(f"`{variable.name}`")
                    res = self.generate_result(info)
                    results.append(res)
        return results

    @classmethod
    def _is_checked_array_length(
        cls, variables: list[LocalVariable], node: Node
    ) -> bool:
        # todo impl node is _is_checked_array_length
        pass

    @classmethod
    def _detect_unchecked_array_length(
        cls, function: FunctionContract
    ) -> Optional[list[Variable]]:
        arr_variables: list[LocalVariable] = [
            param for param in function.parameters if isinstance(param.type, ArrayType)
        ]
        if len(arr_variables) <= 1:
            return
        logger.debug(
            f"function: {function.name} arr: {[item.name for item in arr_variables]}"
        )
        # detect if/require/asset statements
        for node in function.nodes:
            logger.debug(
                f"node: {node.expression} exp type: {type(node.expression)} => {node.type}"
            )
            # check node is `if` BinaryOperation node or `require`/`assert` CallExpression node
            # check irs in node has array length check
            for call in node.internal_calls:
                logger.debug(f"call: {call.name}")
            if (
                isinstance(node.expression, BinaryOperation)
                and node.type == NodeType.IF
            ):
                logger.debug(f"binary expression: {node.expression}")
                if cls._is_checked_array_length(arr_variables, node):
                    return arr_variables
            elif isinstance(node.expression, CallExpression) and any(
                c.name == "assert(bool)" or c.name == "require(bool,string)"
                for c in node.internal_calls
            ):
                logger.debug(f"call expression: {node.expression}")
                if cls._is_checked_array_length(arr_variables, node):
                    return arr_variables


if __name__ == "__main__":
    unittest.main()
