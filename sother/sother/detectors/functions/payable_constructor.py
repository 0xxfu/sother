"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest
from typing import List

from loguru import logger
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class PayableConstructor(AbstractDetector):
    ARGUMENT = "payable-constructor"
    HELP = "Setting the constructor to `payable`"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Setting the constructor to `payable`"
    WIKI_DESCRIPTION = """
You can cut out 10 opcodes in the creation-time EVM bytecode 
if you declare a constructor `payable`. 
Making the constructor `payable` eliminates the need for an initial check 
of `msg.value == 0` and saves `13 gas` on deployment with no security risks.
"""
    WIKI_RECOMMENDATION = """
Set the constructor to `payable`.
"""

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for constructor in contract.constructors:
                if not constructor.payable:
                    result = [
                        constructor,
                        " should be set to `payable` \n",
                    ]
                    res = self.generate_result(result)
                    results.append(res)
        return results


if __name__ == "__main__":
    unittest.main()
