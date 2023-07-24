"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.analyses.data_dependency.data_dependency import is_dependent
from slither.core.cfg.node import Node
from slither.core.declarations import SolidityVariableComposed
from slither.detectors.abstract_detector import DETECTOR_INFO, DetectorClassification
from slither.slithir.operations import Operation, Binary, BinaryType

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings


class IncorrectDeadline(AbstractDetectHasInstance):
    ARGUMENT = "incorrect-deadline"

    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH
    WIKI = DetectorSettings.default_wiki

    HELP = "Incorrect EIP-2612 deadline check"

    WIKI_TITLE = "Incorrect EIP-2612 deadline check"

    WIKI_DESCRIPTION = """
According to [EIP-2612](https://github.com/ethereum/EIPs/blob/71dc97318013bf2ac572ab63fab530ac9ef419ca/EIPS/eip-2612.md?plain=1#L58), 
signatures used on exactly the deadline timestamp are supposed to be allowed. 
While the signature may or may not be used for the exact EIP-2612 use case 
(transfer approvals), for consistency's sake, all deadlines should follow this semantic. 
If the timestamp is an expiration rather than a deadline, 
consider whether it makes more sense to include the expiration timestamp as 
a valid timestamp, as is done for deadlines.
"""
    WIKI_EXPLOIT_SCENARIO = """ """
    WIKI_RECOMMENDATION = """
The current `blocktime` should less than or equal to `deadline`.
```
    // `if` statement
    if (block.timestamp > deadline) {
            revert("deadline");
    }
    
    // Alternative, `require` statement
    require(block.timestamp <= deadline, "deadline");
```
"""

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            node,
            " use at deadlines should be allowed.",
            "\n",
        ]

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        # todo should except `if (): return something` statement
        if (
            ir.node.contains_if()
            and isinstance(ir, Binary)
            and ir.type
            in [
                BinaryType.LESS_EQUAL,
                BinaryType.GREATER_EQUAL,
            ]
        ):
            if ir.type == BinaryType.LESS_EQUAL and is_dependent(
                ir.variable_right, SolidityVariableComposed("block.timestamp"), ir.node
            ):
                return True
            elif ir.type == BinaryType.GREATER_EQUAL and is_dependent(
                ir.variable_left, SolidityVariableComposed("block.timestamp"), ir.node
            ):
                return True
        elif (
            ir.node.contains_require_or_assert()
            and isinstance(ir, Binary)
            and ir.type
            in [
                BinaryType.LESS,
                BinaryType.GREATER,
            ]
        ):
            if ir.type == BinaryType.LESS and is_dependent(
                ir.variable_left, SolidityVariableComposed("block.timestamp"), ir.node
            ):
                return True
            elif ir.type == BinaryType.GREATER and is_dependent(
                ir.variable_right, SolidityVariableComposed("block.timestamp"), ir.node
            ):
                return True

        return False


if __name__ == "__main__":
    unittest.main()
