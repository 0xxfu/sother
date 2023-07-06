"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.core.declarations import FunctionContract
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings
from sother.utils.gas_utils import GasUtils


class EmptyBlock(AbstractDetector):
    ARGUMENT = "empty-block"
    HELP = "Empty blocks should be removed or emit something"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Empty blocks should be removed or emit something"
    WIKI_DESCRIPTION = """
The code should be refactored such that they no longer exist, or the block should do 
something useful, such as emitting an event or reverting. 
If the contract is meant to be extended, the contract should be `abstract` and the function 
signatures be added without any default implementation.
"""

    WIKI_RECOMMENDATION = """
Empty blocks should emit an event, or revert. 
If not, they can simply be removed to save gas upon deployment. 
This is valid for `receive()` functions, but also `constructors()`
"""

    def _detect(self) -> list[Output]:
        results = []

        for contract in self.compilation_unit.contracts_derived:
            if not contract.is_fully_implemented:
                continue
            for function in contract.functions:
                if function.is_empty:
                    json = self.generate_result(
                        [
                            function,
                            " should removed or do something\n",
                        ]
                    )
                    results.append(json)
        return results


if __name__ == "__main__":
    unittest.main()
