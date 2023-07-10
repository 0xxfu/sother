"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from packaging import version
from slither.detectors.abstract_detector import (
    DetectorClassification,
    AbstractDetector,
    DETECTOR_INFO,
)
from slither.detectors.statements.assembly import Assembly
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class UnsafeAssembly(Assembly):
    ARGUMENT = "unsafe-assembly"
    HELP = "Storage Write Removal Bug On Conditional Early Termination"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Storage Write Removal Bug On Conditional Early Termination"

    WIKI_DESCRIPTION = """
In solidity versions 0.8.13 and 0.8.14, there is an 
[optimizer bug](https://github.com/ethereum/solidity-blog/blob/499ab8abc19391be7b7b34f88953a067029a5b45/_posts/2022-06-15-inline-assembly-memory-side-effects-bug.md) where, 
if the use of a variable is in a separate `assembly` block from the block in which it 
was stored, the `mstore` operation is optimized out, leading to uninitialized memory. 
The code currently does not have such a pattern of execution, but it does use `mstore`s 
in `assembly` blocks, so it is a risk for future changes. The affected solidity versions 
should be avoided if at all possible.

See the following for more info:
https://blog.soliditylang.org/2022/09/08/storage-write-removal-before-conditional-termination/

"""

    WIKI_RECOMMENDATION = """
Upgrade pragma to at latest version: https://github.com/ethereum/solidity/releases.
"""
    WIKI_EXPLOIT_SCENARIO = " "

    detect_version = "0.8.14"

    def _detect(self) -> list[Output]:
        results = []
        solc_version = version.parse(self.compilation_unit.solc_version)
        detect_version = version.parse(self.detect_version)
        if solc_version < detect_version:
            for contract in self.compilation_unit.contracts_derived:
                values = self.detect_assembly(contract)
                for func, nodes in values:
                    info: DETECTOR_INFO = [func, " uses assembly\n"]
                    # sort the nodes to get deterministic results
                    nodes.sort(key=lambda x: x.node_id)
                    for node in nodes:
                        info += ["\t- ", node, "\n"]
                    res = self.generate_result(info)
                    results.append(res)

        return results


if __name__ == "__main__":
    unittest.main()
