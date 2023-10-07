"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from slither.core.cfg.node import Node
from slither.core.declarations import Function
from slither.detectors.abstract_detector import DetectorClassification, DETECTOR_INFO
from slither.detectors.operations.unchecked_transfer import (
    UncheckedTransfer as SlitherUncheckedTransfer,
)
from slither.slithir.operations import Operation, HighLevelCall

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings


class UncheckedTransfer(SlitherUncheckedTransfer):
    ARGUMENT = "unchecked-transfer"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.MEDIUM
    HELP = "Return values of `transfer()/transferFrom()` not checked"
    WIKI_TITLE = "Return values of `transfer()/transferFrom()` not checked"
    WIKI_DESCRIPTION = """
Not all `IERC20` implementations `revert()` when there's a failure in `transfer()`/`transferFrom()`. The function signature has a `boolean` return value and they indicate errors that way instead. By not checking the return value, operations that should have marked as failed, may potentially go through without actually making a payment.
"""


# todo except token is state variable
class UnsafeTransfer(AbstractDetectHasInstance):
    ARGUMENT = "unsafe-transfer"

    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.HIGH
    WIKI = DetectorSettings.default_wiki

    HELP = "Unsafe use of `transfer()/transferFrom()` with IERC20"

    WIKI_TITLE = "Unsafe use of `transfer()/transferFrom()` with IERC20"

    WIKI_DESCRIPTION = """
Some tokens do not implement the ERC20 standard properly but are still accepted by most code 
that accepts ERC20 tokens. For example Tether (USDT)'s `transfer()` and `transferFrom()` functions 
on L1 do not return booleans as the specification requires, and instead have no return value. 
When these sorts of tokens are cast to IERC20, their [function signatures](https://medium.com/coinmonks/missing-return-value-bug-at-least-130-tokens-affected-d67bf08521ca) 
do not match and therefore the calls made, revert.
"""
    WIKI_EXPLOIT_SCENARIO = " "
    WIKI_RECOMMENDATION = """
Use [OpenZeppelin’s SafeERC20](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol) 
`safeTransfer()/safeTransferFrom()` instead of `transfer()/transferFrom()`
"""

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            node,
            " should be replaced by `safeTransfer()/safeTransferFrom()`.",
            "\n",
        ]

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        unsafe_transfer_signature: list[str] = [
            "transfer(address,uint256)",
            "transferFrom(address,address,uint256)",
        ]
        if isinstance(ir, HighLevelCall) and isinstance(ir.function, Function):
            return ir.function.solidity_signature in unsafe_transfer_signature
        return False


if __name__ == "__main__":
    unittest.main()
