"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from slither.core.cfg.node import Node
from slither.detectors.abstract_detector import DETECTOR_INFO, DetectorClassification
from slither.slithir.operations import Operation

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
    AbstractTransferInstance,
)
from sother.detectors.detector_settings import DetectorSettings


class ReentrancyTransfer(AbstractDetectHasInstance):
    ARGUMENT = "reentrancy-transfer"
    HELP = "Functions calling contracts/addresses with transfer hooks are missing reentrancy guards"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Functions calling contracts/addresses with transfer hooks are missing reentrancy guards"

    WIKI_DESCRIPTION = """
Even if the function follows the best practice of check-effects-interaction, 
not using a reentrancy guard when there may be transfer hooks will open the 
users of this protocol up to 
[read-only reentrancies](https://chainsecurity.com/curve-lp-oracle-manipulation-post-mortem/) 
with no way to protect against it, except by block-listing the whole protocol.
"""

    WIKI_RECOMMENDATION = """
Using [Reentrancy-Guard](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/security/ReentrancyGuard.sol#L50C5-L62) 
when calling contracts/addresses with transfer hooks.
"""
    WIKI_EXPLOIT_SCENARIO = " "

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        if AbstractTransferInstance.is_erc20_transfer_instance(ir):
            if not any(
                [
                    "nonReentrant" in modifier.name
                    for modifier in ir.node.function.modifiers
                ]
            ):
                return True
        return False

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            node,
            " should use Reentrancy-Guard.",
            "\n",
        ]


if __name__ == "__main__":
    unittest.main()
