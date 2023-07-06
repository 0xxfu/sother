"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest
from typing import List

from loguru import logger
from slither.core.expressions import Literal
from slither.core.solidity_types.elementary_type import Uint, Int
from slither.core.variables import StateVariable
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class ZeroInitializedStateVariable(AbstractDetector):
    ARGUMENT = "zero-initialized-state-variable"
    HELP = "It costs more gas to initialize state variables to zero than to let the default of zero be applied"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "It costs more gas to initialize state variables to zero than to let the default of zero be applied"
    WIKI_DESCRIPTION = """
If a state variable is not set/initialized, 
it is assumed to have the default value (0 for uint, false for bool, address(0) for address…). 
Explicitly initializing it with its default value is an anti-pattern and wastes gas.

More detail see [this.](https://gist.github.com/0xxfu/b111e822aa4ee2e0f6bbaf2658818520)

"""

    WIKI_RECOMMENDATION = """
Do not initialize state variables to zero.
"""

    @classmethod
    def _is_initialized_to_zero(cls, state: StateVariable) -> bool:
        if str(state.type) in Uint + Int:
            if (
                isinstance(state._initial_expression, Literal)
                and state._initial_expression.value == "0"
            ):
                return True

        elif str(state.type) == "address":
            if str(state._initial_expression) == "address(0)":
                return True
        return False

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for state in contract.state_variables_declared:
                if self._is_initialized_to_zero(state):
                    json = self.generate_result(
                        [state, " should not overwrite the default.\n"]
                    )
                    results.append(json)
        return results


if __name__ == "__main__":
    unittest.main()
