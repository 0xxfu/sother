"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.declarations import Function
from slither.core.variables.local_variable import LocalVariable
from slither.detectors.abstract_detector import DetectorClassification, DETECTOR_INFO
from slither.slithir.operations import Operation, HighLevelCall

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings


class UnsupportedDecimalsToken(AbstractDetectHasInstance):
    ARGUMENT = "unsupported-decimals-token"
    HELP = "Unsafe calls to optional ERC20 functions:`decimals()`/`name()`/`symbol()`"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = (
        "Unsafe calls to optional ERC20 functions:`decimals()`/`name()`/`symbol()`"
    )

    WIKI_DESCRIPTION = """
The`decimals()`/`name()`/`symbol()` functions are not a part of the 
[ERC-20 standard](https://eips.ethereum.org/EIPS/eip-20), 
and was added later as an [optional extension](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/extensions/IERC20Metadata.sol). 
As such, some valid ERC20 tokens do not support this interface, 
so it is unsafe to blindly cast all tokens to this interface, 
and then call this function.

"""

    WIKI_RECOMMENDATION = """
Using `safe` call target function. see [this](https://github.com/boringcrypto/BoringSolidity/blob/78f4817d9c0d95fe9c45cd42e307ccd22cf5f4fc/contracts/libraries/BoringERC20.sol#L34-L56) to resolve the issue

For example:
```
    function safeDecimals(IERC20 token) internal view returns (uint8) {
        (bool success, bytes memory data) = address(token).staticcall(abi.encodeWithSelector(SIG_DECIMALS));
        return success && data.length == 32 ? abi.decode(data, (uint8)) : 18;
    }
```
"""
    WIKI_EXPLOIT_SCENARIO = " "

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        return (
            isinstance(ir, HighLevelCall)
            and isinstance(ir.function, Function)
            and ir.function.solidity_signature
            in [
                "name()",
                "symbol()",
                "decimals()",
            ]
            and any([isinstance(var, LocalVariable) for var in ir.read])
        )

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            node,
            " should use `safe` call target function.",
            "\n",
        ]


if __name__ == "__main__":
    unittest.main()
