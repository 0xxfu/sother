"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest
from typing import List

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.declarations import FunctionContract
from slither.core.expressions import (
    UnaryOperation,
    UnaryOperationType,
    AssignmentOperation,
    AssignmentOperationType,
    Literal,
)
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class PrePlusPlus(AbstractDetector):
    ARGUMENT = "pre-plus-plus"
    HELP = "`++i` costs less gas than `i++`, especially when it's used in for-loops (`--i/i--` too)"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "`++i` costs less gas than `i++`, especially when it's used in for-loops (`--i/i--` too)"

    WIKI_DESCRIPTION = """
`++i` costs less gas compared to `i++` or `i += 1` for unsigned integer, as pre-increment is cheaper (about 5 gas per iteration). 
This statement is true even with the optimizer enabled.

`i++` increments i and returns the initial value of i. Which means:
```
uint i = 1;  
i++; // == 1 but i == 2  
```
But ++i returns the actual incremented value:
```
uint i = 1;  
++i; // == 2 and i == 2 too, so no need for a temporary variable  
```
In the first case, the compiler has to create a temporary variable (when used) 
for returning 1 instead of 2
"""

    WIKI_RECOMMENDATION = """
Using `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` to operate the value of an uint variable.

"""

    @classmethod
    def _detect_less_efficient_operate(cls, function: FunctionContract) -> set[Node]:
        result_nodes: set[Node] = set()
        for node in function.nodes:
            if isinstance(node.expression, UnaryOperation) and node.expression.type in [
                UnaryOperationType.PLUSPLUS_POST,
                UnaryOperationType.MINUSMINUS_POST,
            ]:
                result_nodes.add(node)
            elif (
                isinstance(node.expression, AssignmentOperation)
                and node.expression.type
                in [
                    AssignmentOperationType.ASSIGN_ADDITION,
                    AssignmentOperationType.ASSIGN_SUBTRACTION,
                ]
                and isinstance(node.expression.expression_right, Literal)
                and node.expression.expression_right.value == "1"
            ):
                result_nodes.add(node)
        return result_nodes

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for function in contract.functions:
                result_nodes: set[Node] = self._detect_less_efficient_operate(function)
                for node in result_nodes:
                    res = self.generate_result(
                        [
                            node,
                            " should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.\n",
                        ]
                    )
                    results.append(res)
        return results


if __name__ == "__main__":
    unittest.main()
