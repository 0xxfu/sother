"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from slither.core.variables import StateVariable
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.detectors.variables.uninitialized_state_variables import (
    UninitializedStateVarsDetection,
)
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class UnusedStateVariables(AbstractDetector):
    ARGUMENT = "unused-state-variables"
    HELP = "Remove or replace unused state variables"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Remove or replace unused state variables"
    WIKI_DESCRIPTION = """
Saves a storage slot. If the variable is assigned a non-zero value, saves Gsset (20000 gas). If it's assigned a zero value, saves Gsreset (2900 gas). If the variable remains unassigned, there is no gas savings unless the variable is public, in which case the compiler-generated non-payable getter deployment cost is saved. If the state variable is overriding an interface's public function, mark the variable as constant or immutable so that it does not use a storage slot
"""

    WIKI_RECOMMENDATION = """
Remove or replace the unused state variables
"""

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            result_states = self._detect_unused_state(contract)
            for state in result_states:
                json = self.generate_result([state, " is never used."])
                results.append(json)
        return results

    @classmethod
    def _detect_unused_state(cls, contract) -> list[StateVariable]:
        except_states: list[str] = ["__gap"]
        state_variables = contract.state_variables_declared
        written_variables = UninitializedStateVarsDetection._written_variables(contract)
        read_variables = UninitializedStateVarsDetection._read_variables(contract)
        return [
            state
            for state in state_variables
            if state not in read_variables
            and state not in written_variables
            and state.name not in except_states
        ]


if __name__ == "__main__":
    unittest.main()
