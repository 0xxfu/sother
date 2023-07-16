"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from slither.core.cfg.node import Node
from slither.core.declarations import Function
from slither.detectors.abstract_detector import DETECTOR_INFO, DetectorClassification
from slither.slithir.operations import Operation, HighLevelCall

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings


class DeprecatedChainLink(AbstractDetectHasInstance):
    ARGUMENT = "deprecated-chain-link"
    HELP = "Usage of deprecated ChainLink APIs"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Usage of deprecated ChainLink APIs"

    WIKI_DESCRIPTION = """
According to [Chainlink's documentation](https://docs.chain.link/data-feeds/api-reference),
the following functions are deprecated: `latestRound()`/`latestAnswer()`/`latestTimestamp()`/
`getAnswer(uint256 _roundId)`/`getTimestamp(uint256 _roundId)`. 

> This does not error if no
> answer has been reached, it will simply return 0. Either wait to point to
> an already answered Aggregator or use the recommended `getRoundData`
> instead which includes better verification information.

Impact: Deprecated API stops working. 
Prices cannot be obtained. Protocol stops and contracts have to be redeployed.
"""

    WIKI_RECOMMENDATION = """
It is recommended to use `latestRoundData()` method instead of deprecated APIs.
"""

    WIKI_EXPLOIT_SCENARIO = " "

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        return (
            isinstance(ir, HighLevelCall)
            and isinstance(ir.function, Function)
            and ir.function.solidity_signature
            in [
                "latestRound()",
                "latestAnswer()",
                "latestTimestamp()",
                "getAnswer(uint256)",
                "getTimestamp(uint256)",
            ]
        )

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            " should use `latestRoundData()` instead of ",
            node,
            "\n",
        ]


if __name__ == "__main__":
    unittest.main()
