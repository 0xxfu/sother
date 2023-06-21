"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from slither.core.cfg.node import Node
from slither.core.expressions import CallExpression
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class DeprecatedAssert(AbstractDetector):
    ARGUMENT = "deprecated-assert"
    HELP = "`revert CustomError()` should be used instead of `assert()`"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "`revert CustomError()` should be used instead of `assert()`"
    WIKI_DESCRIPTION = """
Prior to solidity version 0.8.0, hitting an assert consumes the **remainder of the transaction's available gas** rather than returning it, as `require()`/`revert()` do. `assert()` should be avoided even past solidity version 0.8.0 as its [documentation](https://docs.soliditylang.org/en/v0.8.19/control-structures.html#panic-via-assert-and-error-via-require) states that "The assert function creates an error of type Panic(uint256). ... Properly functioning code should never create a Panic, not even on invalid external input. If this happens, then there is a bug in your contract which you should fix.

"""

    WIKI_RECOMMENDATION = """
Please use `if (!condition) revert CustomError();` instead of `assert()`.
"""
    WIKI_EXPLOIT_SCENARIO = " "

    def _detect(self) -> List[Output]:
        results = []
        assert_nodes: list[Node] = list()
        for contract in self.compilation_unit.contracts:
            for function in contract.functions:
                for node in function.nodes:
                    if not node.contains_require_or_assert():
                        continue
                    if isinstance(node.expression, CallExpression) and any(
                        c.name == "assert(bool)" for c in node.internal_calls
                    ):
                        assert_nodes.append(node)

        for node in assert_nodes:
            res = self.generate_result(
                [
                    node,
                    " should be replaced by `if (!condition) revert CustomError();`.\n",
                ]
            )
            results.append(res)

        return results

    if __name__ == "__main__":
        unittest.main()
