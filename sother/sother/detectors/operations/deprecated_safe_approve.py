"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.declarations import Function
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.slithir.operations import Operation, HighLevelCall
from slither.utils.output import Output

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings


class DeprecatedSafeApprove(AbstractDetectHasInstance):
    ARGUMENT = "deprecated-safe-approve"
    HELP = "`safeApprove()` is deprecated"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "`safeApprove()` is deprecated"
    WIKI_DESCRIPTION = """
[Deprecated](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/token/ERC20/utils/SafeERC20.sol#L38-L45) 
in favor of `safeIncreaseAllowance()` and `safeDecreaseAllowance()`. 
If only setting the initial allowance to the value that means infinite, 
`safeIncreaseAllowance()` can be used instead. The function may currently work, 
but if a bug is found in this version of OpenZeppelin, and the version that you're 
forced to upgrade to no longer has this function, you'll encounter unnecessary delays 
in porting and testing replacement contracts.

"""

    WIKI_RECOMMENDATION = """
As suggested by the [OpenZeppelin comment](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/token/ERC20/utils/SafeERC20.sol#L38-L45),
replace `safeApprove()` with `safeIncreaseAllowance()` or `safeDecreaseAllowance()` instead.
"""
    WIKI_EXPLOIT_SCENARIO = " "

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        return (
            isinstance(ir, HighLevelCall)
            and isinstance(ir.function, Function)
            and ir.function.solidity_signature
            in ["safeApprove(address,address,uint256)"]
        )

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            node,
            " is deprecated.",
            "\n",
        ]


if __name__ == "__main__":
    unittest.main()
