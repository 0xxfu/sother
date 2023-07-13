"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.core.cfg.node import Node
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.slithir.operations import Operation, SolidityCall
from slither.utils.output import Output

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings


class UseSelfBalance(AbstractDetectHasInstance):
    ARGUMENT = "use-self-balance"
    HELP = "Use `selfbalance()` instead of `address(this).balance`"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Use `selfbalance()` instead of `address(this).balance`"

    WIKI_DESCRIPTION = """
You can use `selfbalance()` instead of `address(this).balance` when 
getting your contract’s balance of ETH to save gas. 
Additionally, you can use `balance(address)` instead of address.balance() when 
getting an external contract’s balance of ETH.
"""

    WIKI_RECOMMENDATION = """
Using `selfbalance()` instead of `address(this).balance`, for example:

```
function assemblyInternalBalance() public returns (uint256) {
    assembly {
        let c := selfbalance()
        mstore(0x00, c)
        return(0x00, 0x20)
    }
}
```
"""

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        return (
            isinstance(ir, SolidityCall)
            and str(ir.expression) == "address(this).balance"
        )

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            "Should use `selfbalance()` instead of ",
            node,
            "\n",
        ]


class UseAssemblyBalance(AbstractDetectHasInstance):
    ARGUMENT = "use-assembly-balance"
    HELP = "Use `balance(address)` instead of address.balance()"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Use `balance(address)` instead of address.balance()"

    WIKI_DESCRIPTION = """
Additionally, you can use `balance(address)` instead of address.balance() when 
getting an external contract’s balance of ETH to save gas.
"""

    WIKI_RECOMMENDATION = """
Use `balance(address)` instead of address.balance(), for example:

```
function assemblyExternalBalance(address addr) public {
    uint256 bal;
    assembly {
        bal := balance(addr)
    }
}
```
"""

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        return (
            isinstance(ir, SolidityCall)
            and ir.function.name == "balance(address)"
            and ir.expression is not None
            and str(ir.expression) != "address(this).balance"
        )

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            "Should use `balance(address)` instead of ",
            node,
            "\n",
        ]


if __name__ == "__main__":
    unittest.main()
