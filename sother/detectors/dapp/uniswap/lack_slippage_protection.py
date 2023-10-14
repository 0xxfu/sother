"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-10
"""
import unittest

from slither.core.cfg.node import Node
from slither.core.declarations import Function, Structure
from slither.core.solidity_types import UserDefinedType
from slither.detectors.abstract_detector import DetectorClassification, DETECTOR_INFO
from slither.slithir.operations import Operation, HighLevelCall

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings


# todo impl amount0Min/amount1Min variables doesn't in if condition
class LackSlippageProtection(AbstractDetectHasInstance):
    ARGUMENT = "lack-slippage-protection"
    HELP = "Lack of slippage protection can lead to significant loss of user funds"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = (
        "Lack of slippage protection can lead to significant loss of user funds"
    )
    WIKI_DESCRIPTION = """
Strategy contracts interact with Uniswap V3 in multiple areas of the code. 
However, none of these interactions contain any slippage control, 
meaning that the contract, and by extension all users who hold shares, 
can lose significant value due to illiquid pools or MEV sandwich attacks every time 
any of the relevant functions are called.

In each of the below instances, a call to Uniswap V3 is made and `amount0Min` and `amount1Min` 
are each set to 0, which allows for **100% slippage tolerance**. 
This means that the action could lead to the caller losing up to 100% of their tokens due to slippage.
"""
    WIKI_EXPLOIT_SCENARIO = " "

    WIKI_RECOMMENDATION = """
For each vulnerable function, allow the caller to specify values 
for `amount0Min` and `amount1Min` instead of setting them to 0.
"""
    function_list = ["mint", "increaseLiquidity", "decreaseLiquidity"]

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        if (
            isinstance(ir, HighLevelCall)
            and isinstance(ir.function, Function)
            and ir.function.name in cls.function_list
            and len(ir.function.parameters) == 1
        ):
            for param in ir.function.parameters:
                param_type = param.type
                if (
                    isinstance(param_type, UserDefinedType)
                    and isinstance(param_type.type, Structure)
                    and all(
                        item in param_type.type.elems.keys()
                        for item in ["amount0Min", "amount1Min"]
                    )
                ):
                    return "amount0Min:0" in str(
                        ir.expression
                    ) and "amount1Min:0" in str(ir.expression)

        return False

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            node,
            " lack of slippage protection.",
            "\n",
        ]


if __name__ == "__main__":
    unittest.main()
