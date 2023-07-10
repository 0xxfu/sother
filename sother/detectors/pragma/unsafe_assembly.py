"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.detectors.abstract_detector import DetectorClassification, AbstractDetector
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


# todo implement
class UnsafeAssembly(AbstractDetector):
    ARGUMENT = "unsafe-floating-pragma"
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

    def _detect(self) -> list[Output]:
        results = []
        return results


if __name__ == "__main__":
    unittest.main()
