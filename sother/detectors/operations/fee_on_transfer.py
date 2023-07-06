"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import Optional

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.declarations import Function
from slither.core.variables import Variable
from slither.detectors.abstract_detector import DetectorClassification, DETECTOR_INFO
from slither.slithir.operations import Operation, HighLevelCall, LibraryCall

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
    AbstractTransferInstance,
)
from sother.detectors.detector_settings import DetectorSettings


class FeeOnTransfer(AbstractTransferInstance):
    ARGUMENT = "fee-on-transfer"
    HELP = "Incompatibility with transfer-on-fee or deflationary tokens"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Incompatibility with transfer-on-fee or deflationary tokens"
    WIKI_DESCRIPTION = """
Some ERC20 tokens make modifications to the standard implementations of
their ERC20’s `transfer` or `balanceOf` functions.
One type of such token is deflationary tokens that charge a fee on every
`transfer()` and `transferFrom()`.
The protocol does not have incompatibility with fee-on-transfer tokens.

Note that there has been a real-world exploit related to this with 
[Balancer pool and STA deflationary tokens](https://medium.com/1inch-network/balancer-hack-2020-a8f7131c980e).
"""
    WIKI_EXPLOIT_SCENARIO = """
i.e. Fee-on-transfer scenario:
1. Contract calls transfer from contractA 100 tokens to current contract
2. Current contract thinks it received 100 tokens
3. It updates balances to increase +100 tokens
4. While actually contract received only 90 tokens
5. That breaks whole math for given token
"""

    WIKI_RECOMMENDATION = """
1. Consider comparing before and after balance to get the actual transferred amount.
2. Alternatively, disallow tokens with fee-on-transfer mechanics to be added as tokens.
"""

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        if not cls.is_transfer_instance(ir):
            return False

        return not cls.is_check_balance_in_function(
            ir.node.function, cls.get_transfer_to(ir)
        )

    @classmethod
    def is_check_balance_in_function(
        cls, function: Function, transfer_to: Optional[Variable]
    ) -> bool:
        if not transfer_to:
            return False
        get_balance_count = 0
        for node in function.nodes:
            for ir in node.irs:
                if not (
                    isinstance(ir, HighLevelCall)
                    and isinstance(ir.function, Function)
                    and ir.function.solidity_signature in ["balanceOf(address)"]
                ):
                    continue
                if ir.arguments[0] == transfer_to:
                    get_balance_count += 1

        return get_balance_count >= 2

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            node,
            " with fee on transfer are not supported.",
            "\n",
        ]


if __name__ == "__main__":
    unittest.main()
