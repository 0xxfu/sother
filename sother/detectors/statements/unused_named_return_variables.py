"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest
from typing import List

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.variables.local_variable import LocalVariable
from slither.detectors.abstract_detector import (
    DetectorClassification,
    DETECTOR_INFO,
    AbstractDetector,
)
from slither.slithir.operations import Operation
from slither.utils.output import Output

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings


class UnusedNamedReturnVariables(AbstractDetector):
    ARGUMENT = "unused-return-name"
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


if __name__ == "__main__":
    unittest.main()
