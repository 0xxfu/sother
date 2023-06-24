"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.declarations import Function
from slither.core.variables import Variable
from slither.detectors.abstract_detector import DetectorClassification, DETECTOR_INFO
from slither.slithir.operations import Operation, HighLevelCall, Condition, Binary

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
    AbstractTransferInstance,
)
from sother.detectors.detector_settings import DetectorSettings


class ZeroCheckWithTransfer(AbstractTransferInstance):
    ARGUMENT = "zero-check-with-transfer"
    HELP = "Amounts should be checked for `0` before calling a `transfer`"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Amounts should be checked for `0` before calling a `transfer`"
    WIKI_DESCRIPTION = """
According to the fact that EIP-20 [states](https://github.com/ethereum/EIPs/blob/46b9b698815abbfa628cd1097311deee77dd45c5/EIPS/eip-20.md?plain=1#L116) that zero-valued transfers must be accepted.

Checking non-zero transfer values can avoid an expensive external call and save gas.
While this is done at some places, it’s not consistently done in the solution.
"""

    WIKI_RECOMMENDATION = """
Consider adding a non-zero-value check at the beginning of function.
"""

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            "Adding a non-zero-value check for ",
            node,
            " at the beginning of ",
            node.function,
            "\n",
        ]

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        if not cls.is_transfer_instance(ir):
            return False
        return not cls.is_check_zero_in_function(
            ir.node.function, cls.get_transfer_amount(ir)
        )

    @classmethod
    def is_check_zero_in_function(cls, function: Function, amount: Variable):
        if not amount:
            return False
        for node in function.nodes:
            for ir in node.irs:
                if not isinstance(ir, Binary):
                    continue
                if (ir.variable_left == amount and ir.variable_right in [0, 1]) or (
                    ir.variable_left in [0, 1] and ir.variable_right == amount
                ):
                    return True


# todo impl
# cause transactions that involve other tokens (such as batch operations) to fully revert
class RevertWithZeroTransfer(ZeroCheckWithTransfer):
    pass


if __name__ == "__main__":
    unittest.main()
