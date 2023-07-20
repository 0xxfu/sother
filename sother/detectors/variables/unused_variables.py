"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from slither.core.variables import StateVariable
from slither.core.variables.local_variable import LocalVariable
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.detectors.variables.uninitialized_state_variables import (
    UninitializedStateVarsDetection,
)
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


# override UnusedStateVars
class UnusedStateVars(AbstractDetector):
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


class UnusedNamedReturnVariables(AbstractDetector):
    ARGUMENT = "unused-named-return-variables"
    HELP = "Not using the named return variables anywhere in the function is confusing"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = (
        "Not using the named return variables anywhere in the function is confusing"
    )

    WIKI_DESCRIPTION = """
Consider changing the variable to be an unnamed one, 
since the variable is never assigned, nor is it returned by name. 
If the optimizer is not turned on, leaving the code as it is will also waste gas 
for the stack variable.
"""

    WIKI_RECOMMENDATION = """
Remove the unused named return variables.
"""

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for function in contract.functions:
                result_vars: set[LocalVariable] = set()
                for return_var in function.returns:
                    if return_var not in function.variables_written:
                        result_vars.add(return_var)
                if len(result_vars) > 0:
                    info: DETECTOR_INFO = [
                        "The named return variables in ",
                        function,
                        " are unused.\n",
                    ]
                    for var in result_vars:
                        info += ["\t- ", var, "\n"]
                    results.append(self.generate_result(info))
        return results
