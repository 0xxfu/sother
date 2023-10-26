"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from slither.core.cfg.node import NodeType
from slither.detectors.abstract_detector import (
    DetectorClassification,
)
from slither.slithir.operations import Length, Operation
from slither.utils.output import Output

from sother.detectors.abstracts.abstract_detect_in_loop import AbstractDetectInLoop
from sother.detectors.detector_settings import DetectorSettings
from sother.utils.gas_utils import GasUtils


class ArrayLengthInLoop(AbstractDetectInLoop):
    ARGUMENT = "array-length-in-loop"
    HELP = "Cache the `<array>.length` for the loop condition"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Cache the `<array>.length` for the loop condition"
    WIKI_DESCRIPTION = """
The overheads outlined below are _PER LOOP_, excluding the first loop
* storage arrays incur a Gwarmaccess (**100 gas**)
* memory arrays use `MLOAD` (**3 gas**)
* calldata arrays use `CALLDATALOAD` (**3 gas**)

Caching the length changes each of these to a `DUP<N>` (**3 gas**), and gets rid of the extra `DUP<N>` needed to store the stack offset.
More detail optimization see [this](https://gist.github.com/0xxfu/80fcbc39d2d38d85ae61b4b8838ef30b)
"""

    WIKI_RECOMMENDATION = """
Caching the `<array>.length` for the loop condition, for example:
```solidity
// gas save (-230)
function loopArray_cached(uint256[] calldata ns) public returns (uint256 sum) {
    uint256 length = ns.length;
    for(uint256 i = 0; i < length;) {
        sum += ns[i];
        unchecked {
            ++i;
        }
    }
}
```
"""

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        # except `array.pop()`
        return isinstance(ir, Length) and ir.node.type == NodeType.IFLOOP

    def _detect(self) -> List[Output]:
        results = []

        result_nodes = self.detect_loop_in_function(
            GasUtils.get_available_functions(self.compilation_unit)
        )
        for node in result_nodes:
            res = self.generate_result([node, " `<array>.length` should be cached.\n"])
            results.append(res)

        return results


if __name__ == "__main__":
    unittest.main()
