"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest
from typing import List

from slither.core.cfg.node import Node
from slither.core.declarations import Contract
from slither.detectors.abstract_detector import (
    DetectorClassification,
    AbstractDetector,
    DETECTOR_INFO,
)
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

    def _detect_zero_address_check(self, contract: Contract) -> set[Node]:
        # todo implement
        pass

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
