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
)
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class ImmutableInUpgradeable(AbstractDetector):
    ARGUMENT = "immutable-in-upgradeable"
    HELP = "Immutable variables used in upgradable contracts may cause DoS"
    IMPACT = DetectorClassification.INFORMATIONAL
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Immutable variables used in upgradable contracts may cause DoS"
    WIKI_DESCRIPTION = """
The upgradeable contracts have some variables defined as immutable which are set during the constructor call.
This may probably work during the first deployment, but once the contract needs to be updated, the initialize
function needs to be called, and since the immutable variables are stored in the contract bytecode, 
the new upgradeable contracts will not retain these changes.
As a result, making the upgraded contract useless causing DoS.

References by OpenZeppelin for the Issue and Fix:
1. https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#avoid-initial-values-in-field-declarations
2. https://docs.openzeppelin.com/upgrades-plugins/1.x/faq#why-cant-i-use-immutable-variables
"""

    WIKI_RECOMMENDATION = """
Remove the `immutable` keyword and move the constructor logic to initialize function.
"""
    WIKI_EXPLOIT_SCENARIO = " "

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts:
            if not contract.is_upgradeable:
                continue
            for state in contract.state_variables_declared:
                if state.is_immutable:
                    res = self.generate_result(
                        [
                            "`immutable` keyword of ",
                            state,
                            " should be removed.\n",
                        ]
                    )
                    results.append(res)

        return results


if __name__ == "__main__":
    unittest.main()
