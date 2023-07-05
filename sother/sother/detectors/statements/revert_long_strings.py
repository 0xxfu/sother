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
from slither.core.expressions import CallExpression, Literal
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class RevertLongStrings(AbstractDetector):
    ARGUMENT = "revert-long-strings"
    HELP = "Shortening revert strings to fit in 32 `bytes`"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Shortening revert strings to fit in 32 `bytes`"
    WIKI_DESCRIPTION = """
In Solidity, the size of a string is not fixed and depends on the length of the string. 
Each character in a string requires 2 `bytes` of storage. 
Additionally, there is an overhead of 32 `bytes` to store the length of the string.

Shortening revert strings to fit in 32 bytes will decrease deployment time gas 
and will decrease runtime gas when the revert condition is met.
"""

    WIKI_RECOMMENDATION = """
Shortening revert strings to fit in 32 `bytes`
"""

    @classmethod
    def _contains_require_or_revert(cls, node: Node) -> bool:
        return any(
            c.name in ["require(bool,string)", "revert(string)"]
            for c in node.internal_calls
        )

    @classmethod
    def _detect_revert_long_string(cls, function: FunctionContract) -> set[Node]:
        result_nodes: set[Node] = set()
        for node in function.nodes:
            node_exp = node.expression
            if cls._contains_require_or_revert(node) and isinstance(
                node_exp, CallExpression
            ):
                for arg in node_exp.arguments:
                    if not isinstance(arg, Literal):
                        continue
                    if str(arg.type) == "string" and len(arg.value) > 16:
                        result_nodes.add(node)
        return result_nodes

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for function in contract.functions:
                result_nodes: set[Node] = self._detect_revert_long_string(function)
                for node in result_nodes:
                    res = self.generate_result(
                        [
                            node,
                            " should be shortened strings to fit in 32 `bytes` (16 characters).\n",
                        ]
                    )
                    results.append(res)
        return results


if __name__ == "__main__":
    unittest.main()
