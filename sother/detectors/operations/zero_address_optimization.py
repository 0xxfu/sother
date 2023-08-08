"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest
from typing import List

from slither.core.cfg.node import Node
from slither.core.declarations import Contract
from slither.core.solidity_types import ElementaryType
from slither.detectors.abstract_detector import (
    DetectorClassification,
    AbstractDetector,
    DETECTOR_INFO,
)
from slither.slithir.operations import Binary, TypeConversion
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class ZeroAddressOptimization(AbstractDetector):
    ARGUMENT = "zero-address-optimization"
    HELP = "Use assembly to check for `address(0)`"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Use assembly to check for `address(0)`"
    WIKI_DESCRIPTION = """
[Inline Assembly](https://docs.soliditylang.org/en/latest/assembly.html) more gas efficient and [Saving Gas with Simple Inlining](https://blog.soliditylang.org/2021/03/02/saving-gas-with-simple-inliner/).

"""

    WIKI_RECOMMENDATION = """
Use assembly to check for `address(0)`:

```
function addrNotZero(address _addr) public pure {
        assembly {
            if iszero(_addr) {
                mstore(0x00, "zero address")
                revert(0x00, 0x20)
            }
        }
}
```
"""

    @classmethod
    def _is_zero_address_in_binary_node(cls, node: Node) -> bool:
        zero_address_ir = None
        for ir in node.irs:
            if (
                isinstance(ir, TypeConversion)
                and ir.type == ElementaryType("address")
                and ir.variable == 0
            ):
                zero_address_ir = ir.lvalue
            if isinstance(ir, Binary):
                if zero_address_ir and (
                    ir.variable_left == zero_address_ir
                    or ir.variable_right == zero_address_ir
                ):
                    return True
        return False

    def _detect_zero_address_check(self, contract: Contract) -> set[Node]:
        result_node: set[Node] = set()
        for function in contract.functions:
            for node in function.nodes:
                # if not `require/asset` or `if` expression
                if node.contains_if() or node.contains_require_or_assert():
                    if self._is_zero_address_in_binary_node(node):
                        result_node.add(node)

        return result_node

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            zero_address_validations = self._detect_zero_address_check(contract)
            for node in zero_address_validations:
                info: DETECTOR_INFO = [
                    node,
                    " should use assembly to check for `address(0)`\n",
                ]
                res = self.generate_result(info)
                results.append(res)
        return results


if __name__ == "__main__":
    unittest.main()
