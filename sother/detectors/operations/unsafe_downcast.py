"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.declarations import FunctionContract
from slither.core.expressions import AssignmentOperation
from slither.core.solidity_types.elementary_type import Uint, Int
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.slithir.operations import Assignment
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


# todo implement
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
                if function.name not in ["bad"]:
                    continue
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
    def _detect_unsafe_downcast(cls, function: FunctionContract) -> set[Node]:
        result_nodes: set[Node] = set()
        for node in function.nodes:
            for ir in node.irs:
                if isinstance(ir, Assignment) and str(ir.rvalue.type) in Uint + Int:
                    right_var = ir.rvalue
                    logger.debug(
                        f"node: {node.expression}"
                        f"\nright: {right_var}  right t: {type(right_var.type)} type: {right_var.type}"
                    )
        return result_nodes


if __name__ == "__main__":
    unittest.main()
