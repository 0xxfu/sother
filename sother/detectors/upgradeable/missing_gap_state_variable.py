"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class MissingGapStateVariable(AbstractDetector):
    ARGUMENT = "missing-gap-state-variable"
    HELP = "Upgradeable contract is missing a `__gap` storage variable to allow for new storage variables in later versions"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Upgradeable contract is missing a `__gap` storage variable to allow for new storage variables in later versions"
    WIKI_DESCRIPTION = """
See [this](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#storage-gaps) link for a description of this storage variable. While some contracts may not currently be sub-classed, adding the variable now protects against forgetting to add it in the future.

"""

    WIKI_EXPLOIT_SCENARIO = """ """

    WIKI_RECOMMENDATION = """
It is considered a best practice in upgradeable contracts to include a
state variable named `__gap`. This `__gap` state variable will be used as a
reserved space for future upgrades. It allows adding new state variables
freely in the future without compromising the storage compatibility with
existing deployments.
The size of the `__gap` array is usually calculated so that the amount of
storage used by a contract always adds up to the same number (usually 50
storage slots).

```
contract Contract {
    ...
    
    # declare `__gap` variable at the end of all states
    uint256[50] private __gap;
}
```

"""

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts:
            if not contract.is_upgradeable:
                continue
            # All state variables
            if not any(
                "__gap" == state.name for state in contract.state_variables_ordered
            ):
                info: DETECTOR_INFO = [
                    contract,
                    " is an upgradeable contract that miss `__gap` to allow for new storage variables.",
                ]
                res = self.generate_result(info)
                results.append(res)

        return results


if __name__ == "__main__":
    unittest.main()
