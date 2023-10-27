"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from slither.core.cfg.node import Node
from slither.core.declarations import Function
from slither.detectors.abstract_detector import DetectorClassification, DETECTOR_INFO
from slither.slithir.operations import Operation, HighLevelCall

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings
from sother.utils.function_utils import FunctionUtils


class DeprecatedApprove(AbstractDetectHasInstance):
    ARGUMENT = "deprecated-approve"
    HELP = "`Approve` Race Condition"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "`Approve` Race Condition"
    WIKI_DESCRIPTION = """
The standard ERC20 implementation contains a widely-known racing condition in its approve function, wherein a spender is able to witness the token owner broadcast a transaction altering their approval and quickly sign and broadcast a transaction using to move the current approved amount from the owner’s balance to the spender. If the
spender’s transaction is validated before the owner’s, the spender will be able to get both approval amounts of both transactions.

It is also mentioned in the [EIP-20](https://eips.ethereum.org/EIPS/eip-20):

> NOTE: To prevent attack vectors like the one described here and discussed here, clients SHOULD make sure to create user interfaces in such a way that they set the allowance first to 0 before setting it to another value for the same spender. THOUGH The contract itself shouldn’t enforce it, to allow backwards compatibility with contracts deployed before

More detail see [here](https://docs.google.com/document/d/1YLPtQxZu1UAvO9cZ1O2RPXBbT0mooh4DYKjA_jp-RLM) and [here](https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729).
"""
    WIKI_EXPLOIT_SCENARIO = """ """

    WIKI_RECOMMENDATION = """
Use OpenZeppelin's [increaseAllowance](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/7c8b7a27284f503ce8ae23d63ac9403096dcf6fe/contracts/token/ERC20/utils/SafeERC20.sol#L52-L55) and [decreaseAllowance](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/7c8b7a27284f503ce8ae23d63ac9403096dcf6fe/contracts/token/ERC20/utils/SafeERC20.sol#L61-L69) functions to modify the approval amount instead of using the `approve()` function to modify it.
"""

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        if ir.node.function.is_constructor or ir.node.function.is_constructor_variables:
            return False
        if (
            isinstance(ir, HighLevelCall)
            and isinstance(ir.function, Function)
            and ir.function.solidity_signature in ["approve(address,uint256)"]
            # only include destination come from param
            and FunctionUtils.is_local_var_dependent_param(
                ir.destination, ir.node.function
            )
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
