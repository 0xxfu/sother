"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from slither.detectors.abstract_detector import (
    DetectorClassification,
    AbstractDetector,
    DETECTOR_INFO,
)
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class UpgradeableUninitialized(AbstractDetector):
    ARGUMENT = "upgradeable-uninitialized"
    HELP = "Upgradeable contract not initialized"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Upgradeable contract not initialized"
    WIKI_DESCRIPTION = """
Upgradeable contracts are initialized via an initializer function rather than by a constructor. 
Leaving such a contract uninitialized may lead to it being taken over by a malicious user
"""

    WIKI_EXPLOIT_SCENARIO = """ """

    WIKI_RECOMMENDATION = """
Consider initializing function in the related section.

```
contract Contract {
    ...
    # 
    function initialize() public initializer {
        OwnableUpgradeable.__Ownable_init();
        __ReentrancyGuard_init();
    }

}
```
"""

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts:
            if not contract.is_upgradeable:
                continue
            if not any(
                "initialize" == function.name
                for function in contract.functions_declared
            ):
                info: DETECTOR_INFO = [
                    contract,
                    " is an upgradeable contract that does not initialized",
                ]
                res = self.generate_result(info)
                results.append(res)

        return results


if __name__ == "__main__":
    unittest.main()
