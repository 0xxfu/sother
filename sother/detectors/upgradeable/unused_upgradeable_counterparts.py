"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.core.declarations import Contract
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class UnusedUpgradeableCounterparts(AbstractDetector):
    ARGUMENT = "unused-upgradeable-counterparts"
    HELP = "Contracts are not using their OZ Upgradeable counterparts"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Contracts are not using their OZ Upgradeable counterparts"
    WIKI_DESCRIPTION = """
The non-upgradeable standard version of OpenZeppelin’s library are inherited 
by the contracts. It would be safer to use the upgradeable versions of the library contracts 
to avoid unexpected behaviour.
"""

    WIKI_EXPLOIT_SCENARIO = """ """

    WIKI_RECOMMENDATION = """
Where applicable, use the contracts from `@openzeppelin/contracts-upgradeable` instead 
of `@openzeppelin/contracts`. See https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/tree/master/contracts 
for list of available upgradeable contracts
"""

    def _detect(self) -> list[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            result_inherits: set[Contract] = set()
            if not contract.is_upgradeable:
                continue
            for inherit in contract.inheritance:
                if inherit.name != "Initializable" and not inherit.is_upgradeable:
                    result_inherits.add(inherit)

            if len(result_inherits) <= 0:
                continue
            info: DETECTOR_INFO = [
                contract,
                " should inherit upgradeable contract instead of following non-upgradeable contracts:\n",
            ]
            for inherit in result_inherits:
                info += ["\t- ", inherit, "\n"]
            res = self.generate_result(info)
            results.append(res)

        return results


if __name__ == "__main__":
    unittest.main()
