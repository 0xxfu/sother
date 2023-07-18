"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.declarations import Function
from slither.detectors.abstract_detector import DETECTOR_INFO, DetectorClassification
from slither.slithir.operations import Operation, HighLevelCall

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings


class ReentrancySendValue(AbstractDetectHasInstance):
    ARGUMENT = "reentrancy-send-value"
    HELP = "Missing Reentrancy-Guard when using `sendValue` from OZ's `Address.sol`"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = (
        "Missing Reentrancy-Guard when using `sendValue` from OZ's `Address.sol`"
    )

    WIKI_DESCRIPTION = """
OZ’s Address.sol library is used. Ether transfer is done with a `sendValue` call in 
the following functions.

There is this warning in OZ’s Address.sol library. Accordingly, he used the 
Check-Effect-Interaction pattern in the project:
```solidity
    * IMPORTANT: because control is transferred to `recipient`, care must be
    * taken to not create reentrancy vulnerabilities. Consider using
    * {ReentrancyGuard} or the
    * https://solidity.readthedocs.io/en/v0.5.11/security-considerations.html#use-the-checks-effects-interactions-pattern[checks-effects-interactions pattern].
    */
```

It would be best practice to use re-entrancy Guard for reasons such as complicated 
dangers such as view Re-Entrancy that emerged in the last period and the possibility 
of expanding the project and its integration with other contracts.
"""

    WIKI_RECOMMENDATION = """
Using [Reentrancy-Guard](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/security/ReentrancyGuard.sol#L50C5-L62) 
when using `sendValue` from OZ's `Address.sol`.
"""
    WIKI_EXPLOIT_SCENARIO = " "

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        # todo detect ReentrancyGuard modifier name isn't nonReentrant
        return (
            isinstance(ir, HighLevelCall)
            and isinstance(ir.function, Function)
            and ir.function.solidity_signature in ["sendValue(address,uint256)"]
            and not any(
                [
                    "nonReentrant" in modifier.name
                    for modifier in ir.node.function.modifiers
                ]
            )
        )

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            node,
            " should use Reentrancy-Guard.",
            "\n",
        ]


if __name__ == "__main__":
    unittest.main()
