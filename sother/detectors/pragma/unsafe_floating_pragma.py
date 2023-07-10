"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class UnsafeFloatingPragma(AbstractDetector):
    ARGUMENT = "unsafe-floating-pragma"
    HELP = "Unsafe to use floating pragma"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Unsafe to use floating pragma"

    WIKI_DESCRIPTION = """
Contracts should be deployed with the same compiler version and flags that 
they have been tested with thoroughly. 
Locking the pragma helps to ensure that contracts do not accidentally get deployed using, 
for example, an outdated compiler version that might introduce bugs that affect the 
contract system negatively.

More detail see [SWC-103](https://swcregistry.io/docs/SWC-103).
"""

    WIKI_RECOMMENDATION = """
Lock the pragma version and also consider known bugs (https://github.com/ethereum/solidity/releases) 
for the compiler version that is chosen.
"""
    WIKI_EXPLOIT_SCENARIO = " "

    def _detect(self) -> list[Output]:
        results = []
        for pragma in self.compilation_unit.pragma_directives:
            if "^" in pragma.version:
                result = self.generate_result(
                    [
                        f"Should lock the pragma version instead of floating pragma: ",
                        pragma,
                        ". \n",
                    ]
                )
                results.append(result)
        return results


if __name__ == "__main__":
    unittest.main()
