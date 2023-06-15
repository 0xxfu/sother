"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List, Optional

from loguru import logger
from slither.core.cfg.node import Node, NodeType
from slither.core.declarations import FunctionContract
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
)
from slither.slithir.operations import InternalCall, Length
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings
from sother.utils.gas_utils import GasUtils


def detect_array_length_loop(functions: list[FunctionContract]) -> list[Node]:
    ret: List[Node] = []
    for func in functions:
        array_length_in_loop(func.entry_point, 0, [], ret)
    return ret


def array_length_in_loop(
    node: Optional[Node],
    in_loop_counter: int,
    visited: List[Node],
    ret: List[Node],
) -> None:
    if node is None:
        return

    if node in visited:
        return
    # shared visited
    visited.append(node)

    # check loop start and end
    if node.type == NodeType.STARTLOOP:
        in_loop_counter += 1
    elif node.type == NodeType.ENDLOOP:
        in_loop_counter -= 1

    if in_loop_counter > 0:
        for ir in node.all_slithir_operations():
            if isinstance(ir, Length):
                ret.append(ir.node)
                break
            if isinstance(ir, (InternalCall)) and ir.function:
                array_length_in_loop(
                    ir.function.entry_point, in_loop_counter, visited, ret
                )

    for son in node.sons:
        array_length_in_loop(son, in_loop_counter, visited, ret)


class LoopArrayLength(AbstractDetector):
    ARGUMENT = "loop-array-length"
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
            i++;
        }
    }
}
```
"""

    def _detect(self) -> List[Output]:
        results = []

        result_nodes = detect_array_length_loop(
            GasUtils.get_available_functions(self.compilation_unit)
        )
        for node in result_nodes:
            logger.debug(f"length in loop: {str(node)}")
            res = self.generate_result(
                [node, " `<array>.length` should be cached.\n"]
            )
            results.append(res)

        return results


if __name__ == "__main__":
    unittest.main()
