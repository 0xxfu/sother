"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.declarations import Function
from slither.detectors.abstract_detector import DetectorClassification, DETECTOR_INFO
from slither.slithir.operations import Operation, HighLevelCall
from slither.slithir.variables import TemporaryVariable

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings


class RevertOnApproveMax(AbstractDetectHasInstance):
    ARGUMENT = "revert-on-approve-max"
    HELP = "Approve `type(uint256).max` not work with some tokens"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Approve `type(uint256).max` not work with some tokens"

    WIKI_DESCRIPTION = """
Some tokens (e.g. `UNI`, `COMP`) revert if the value passed to `approve` or `transfer` 
is larger than `uint96`.

Both of the above tokens have special case logic in `approve` that sets `allowance` 
to `type(uint96).max` if the `approval` amount is `uint256(-1)`, which may cause 
issues with systems that expect the value passed to `approve` to be reflected in 
the allowances mapping.

Approving the maximum value of `uint256` is a known practice to save gas. 
However, this pattern was proven to increase the impact of an attack many times in the past, 
in case the approved contract gets hacked.
"""

    WIKI_RECOMMENDATION = """
Consider approving the exact amount that’s needed to be transferred 
instead of the `type(uint256).max` amount.
"""
    WIKI_EXPLOIT_SCENARIO = " "

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        return (
            isinstance(ir, HighLevelCall)
            and isinstance(ir.function, Function)
            and ir.function.solidity_signature
            in [
                "approve(address,uint256)",
                "safeApprove(address,address,uint256)",
                "forceApprove(address,address,uint256)",
                "safeIncreaseAllowance(address,address,uint256)",
            ]
            and "type()(uint256).max" in str(ir.node.expression)
        )

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            node,
            " should use exact amount that's needed to be transferred.",
            "\n",
        ]


if __name__ == "__main__":
    unittest.main()
