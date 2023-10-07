"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from collections import defaultdict
from typing import List

from slither.core.declarations import Contract, Function
from slither.detectors.abstract_detector import (
    DetectorClassification,
    DETECTOR_INFO,
    AbstractDetector,
)
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class OwnerCentralization(AbstractDetector):
    ARGUMENT = "owner-centralization"
    HELP = "The owner is a single point of failure and a centralization risk"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "The owner is a single point of failure and a centralization risk"
    WIKI_DESCRIPTION = """
Having a single EOA as the only owner of contracts is a large centralization risk and a single point of failure. A single private key may be taken in a hack, or the sole holder of the key may become unable to retrieve the key when necessary.

There are several privileged entities that have access to sensitive operations as follows.
"""

    WIKI_RECOMMENDATION = """
Add a time lock to critical functions. Admin-only functions that change critical parameters should emit events and have timelocks.
Events allow capturing the changed parameters so that off-chain tools/interfaces can register such changes with timelocks that allow users to evaluate them and consider if they would like to engage/exit based on how they perceive the changes as affecting the trustworthiness of the protocol or profitability of the implemented financial services.

Allow only multi-signature wallets to call the function to reduce the likelihood of an attack.
"""
    WIKI_EXPLOIT_SCENARIO = " "

    @classmethod
    def _is_owner_modifier(cls, modifier: Contract | Function) -> bool:
        return "onlyOwner" in modifier.name

    def _detect(self) -> List[Output]:
        results = []
        modifier_functions: dict[Contract | Function, list[Function]] = defaultdict(
            list
        )
        for contract in self.compilation_unit.contracts:
            for function in contract.functions_declared:
                for modifier in function.modifiers:
                    if not self._is_owner_modifier(modifier):
                        continue
                    modifier_functions[modifier].append(function)

        for modifier in modifier_functions:
            info: DETECTOR_INFO = [
                "The role ",
                modifier,
                " is a single point of failure and a centralization risk. "
                "and have access to sensitive operations as follows:\n",
            ]
            for function in modifier_functions[modifier]:
                info += ["\t- ", function, "\n"]
            res = self.generate_result(info)
            results.append(res)
        return results


if __name__ == "__main__":
    unittest.main()
