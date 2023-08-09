"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from slither.core.cfg.node import Node
from slither.core.declarations import Function
from slither.core.variables.local_variable import LocalVariable
from slither.detectors.abstract_detector import DetectorClassification, DETECTOR_INFO
from slither.slithir.operations import Operation, HighLevelCall

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings


class DeprecatedApprove(AbstractDetectHasInstance):
    ARGUMENT = "deprecated-approve"
    HELP = "Did not Approve to zero first"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Did not Approve to zero first"
    WIKI_DESCRIPTION = """
Calling `approve()` without first calling `approve(0)` if the current approval is non-zero 
will revert with some tokens, such as Tether (USDT). While Tether is known to do this, 
it applies to other tokens as well, which are trying to protect against 
[this attack vector](https://docs.google.com/document/d/1YLPtQxZu1UAvO9cZ1O2RPXBbT0mooh4DYKjA_jp-RLM/edit). 
`safeApprove()` itself also implements this protection.
Always reset the approval to zero before changing it to a new value, 
or use `safeIncreaseAllowance()`/`safeDecreaseAllowance()`

"""
    WIKI_EXPLOIT_SCENARIO = """
Some ERC20 tokens like `USDT` require resetting the approval to 0 first before being 
able to reset it to another value.

Unsafe ERC20 approve that do not handle non-standard erc20 behavior.
1. Some token contracts do not return any value.
2. Some token contracts revert the transaction when the allowance is not zero.
"""

    WIKI_RECOMMENDATION = """
As suggested by the [OpenZeppelin comment](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/token/ERC20/utils/SafeERC20.sol#L38-L45),
replace `approve()/safeApprove()` with `safeIncreaseAllowance()` or `safeDecreaseAllowance()` instead.
"""

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        if (
            isinstance(ir, HighLevelCall)
            and isinstance(ir.function, Function)
            and ir.function.solidity_signature in ["approve(address,uint256)"]
            # only include destination come from param
            and isinstance(ir.destination, LocalVariable)
            and ir.destination in ir.node.function.parameters
        ):
            return True
        return False

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            node,
            " should be used `safeIncreaseAllowance()` or `safeDecreaseAllowance()` instead.",
            "\n",
        ]


if __name__ == "__main__":
    unittest.main()
