"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.core.cfg.node import Node
from slither.detectors.abstract_detector import DetectorClassification, DETECTOR_INFO
from slither.slithir.operations import Operation, SolidityCall

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings


class UnsafeTxOrigin(AbstractDetectHasInstance):
    ARGUMENT = "unsafe-tx-origin"
    HELP = "Use of `tx.origin` is unsafe in almost every context"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Use of `tx.origin` is unsafe in almost every context"

    WIKI_DESCRIPTION = """
According to [Vitalik Buterin](https://ethereum.stackexchange.com/questions/196/how-do-i-make-my-dapp-serenity-proof), 
contracts should _not_ `assume that tx.origin will continue to be usable or meaningful`. 
An example of this is [EIP-3074](https://eips.ethereum.org/EIPS/eip-3074#allowing-txorigin-as-signer-1) 
which explicitly mentions the intention to change its semantics when it's used with new op 
codes. There have also been calls to 
[remove](https://github.com/ethereum/solidity/issues/683) `tx.origin`, 
and there are [security issues](https://docs.soliditylang.org/en/latest/security-considerations.html#tx-origin) 
associated with using it for authorization. 

For these reasons, it's best to completely avoid the feature.
"""

    WIKI_RECOMMENDATION = """
Please use `msg.sender` instead of `tx.origin` as much as possible.
"""
    WIKI_EXPLOIT_SCENARIO = " "

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        return "tx.origin" in str(ir.expression)

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            node,
            " should use `msg.sender` instead of `tx.origin` as much as possible.",
            "\n",
        ]


if __name__ == "__main__":
    unittest.main()
