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


class LackDeadlineForUniswap(AbstractDetectHasInstance):
    ARGUMENT = "lack-deadline-in-uniswap"
    HELP = "Lack of deadline for Uniswap AMM"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Lack of deadline for Uniswap AMM"
    WIKI_DESCRIPTION = """
There is no deadline parameter in the Uniswap param struct. It can caused a lot of serious problems:

1. Alice wants to swap eth for safEth
2. The transaction is submitted to the mempool, however, Alice chose a transaction fee that is too low for miners to be interested in including her transaction in a block. The transaction stays pending in the mempool for extended periods, which could be hours, days, weeks, or even longer.
3. When the average gas fee dropped far enough for Alice's transaction to become interesting again for miners to include it, her swap will be executed. In the meantime, the price of ETH could have drastically changed. She will still get 1 ETH but the safEth value of that output might be significantly lower. She has unknowingly performed a bad trade due to the pending transaction she forgot about.

An even worse way this issue can be maliciously exploited is through MEV:

1. The swap transaction is still pending in the mempool. Average fees are still too high for miners to be interested in it. The price of tokens has gone up significantly since the transaction was signed, meaning Alice would receive a lot more ETH when the swap is executed. But that also means that her maximum slippage value (sqrtPriceLimitX96 and minOut ) is outdated and would allow for significant slippage.
2. A MEV bot detects the pending transaction. Since the outdated maximum slippage value now allows for high slippage, the bot sandwiches Alice, resulting in significant profit for the bot and significant loss for Alice.

Also for the same reason it is necessary to provide the user to pass in the slippage to prevent something like this too.
"""
    WIKI_EXPLOIT_SCENARIO = " "

    WIKI_RECOMMENDATION = """
Function should accept a user-input deadline param that should be passed along to Uniswap param struct.
"""

    function_list = [
        "exactInputSingle",
        "exactInput",
        "exactOutputSingle",
        "exactOutput",
    ]

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
                if isinstance(param_type, UserDefinedType) and isinstance(
                    param_type.type, Structure
                ):
                    return all(
                        [item != "deadline" for item in param_type.type.elems.keys()]
                    )
        return False

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            node,
            " lack of deadline for Uniswap AMM.",
            "\n",
        ]


if __name__ == "__main__":
    unittest.main()
