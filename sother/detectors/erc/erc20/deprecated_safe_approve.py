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
    HELP = "`safeApprove()` is deprecated due to `Approve` Race Condition"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "`safeApprove()` is deprecated due to `Approve` Race Condition"
    WIKI_DESCRIPTION = """
[Deprecated](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/token/ERC20/utils/SafeERC20.sol#L38-L45) 
in favor of `safeIncreaseAllowance()` and `safeDecreaseAllowance()`. 

The standard ERC20 implementation contains a widely-known racing condition in its approve function, wherein a spender is able to witness the token owner broadcast a transaction altering their approval and quickly sign and broadcast a transaction using to move the current approved amount from the owner’s balance to the spender. If the
spender’s transaction is validated before the owner’s, the spender will be able to get both approval amounts of both transactions.

It is also mentioned in the [EIP-20](https://eips.ethereum.org/EIPS/eip-20):

> NOTE: To prevent attack vectors like the one described here and discussed here, clients SHOULD make sure to create user interfaces in such a way that they set the allowance first to 0 before setting it to another value for the same spender. THOUGH The contract itself shouldn’t enforce it, to allow backwards compatibility with contracts deployed before

More detail see [here](https://docs.google.com/document/d/1YLPtQxZu1UAvO9cZ1O2RPXBbT0mooh4DYKjA_jp-RLM) and [here](https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729).
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
            " is deprecated due to `Approve` Race Condition.",
            "\n",
        ]


if __name__ == "__main__":
    unittest.main()
