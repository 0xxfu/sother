"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from loguru import logger
from slither.core.variables import StateVariable
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
)
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class PublicToPrivateConstant(AbstractDetector):
    ARGUMENT = "public-to-private-constant"
    HELP = "Using `private` rather than `public` for constants, saves gas"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = (
        "Using `private` rather than `public` for constants, saves gas"
    )
    WIKI_DESCRIPTION = """
If needed, the values can be read from the verified contract source code, or if there are multiple values there can be a single getter function that [returns a tuple](https://github.com/code-423n4/2022-08-frax/blob/90f55a9ce4e25bceed3a74290b854341d8de6afa/src/contracts/FraxlendPair.sol#L156-L178) of the values of all currently-public constants. 

Saves **3406-3606 gas** in deployment gas due to the compiler not having to create non-payable getter functions for deployment calldata, not having to store the bytes of the value outside of where it's used, and not adding another entry to the method ID table
"""

    WIKI_RECOMMENDATION = """
Using `private` replace `public` with constant.
"""

    def _detect(self) -> List[Output]:
        results = []
        public_constants: list[StateVariable] = []
        for state in self.compilation_unit.state_variables:
            if state.is_constant and state.visibility == "public":
                public_constants.append(state)
                logger.debug(f"public constants: {state}")
        for variable in public_constants:
            res = self.generate_result(
                [
                    variable,
                    " should be used `private` visibility to save gas.\n",
                ]
            )
            results.append(res)
        return results


if __name__ == "__main__":
    unittest.main()
