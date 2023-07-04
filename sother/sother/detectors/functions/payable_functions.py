"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest
from typing import List

from loguru import logger
from slither.core.declarations import FunctionContract
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


class PayableFunction(AbstractDetector):
    ARGUMENT = "payable-function"
    HELP = "Functions guaranteed to revert when called by normal users can be marked `payable`"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Functions guaranteed to revert when called by normal users can be marked `payable`"
    WIKI_DESCRIPTION = """
If a function modifier such as `onlyOwner/onlyAdmin/only**` is used, 
the function will revert if a normal user tries to pay the function. 
Marking the function as payable will lower the gas cost for legitimate callers 
because the compiler will not include checks for whether a payment was provided. 

The extra opcodes avoided are `CALLVALUE(2)`,`DUP1(3)`,`ISZERO(3)`,`PUSH2(3)`,
`JUMPI(10)`,`PUSH1(3)`,`DUP1(3)`,`REVERT(0)`,`JUMPDEST(1)`,`POP(2)`, 
which costs an average of about `21 gas` per call to the function, 
in addition to the extra deployment cost
"""
    WIKI_RECOMMENDATION = """
Set the function to `payable`.
"""

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            result_functions: set[FunctionContract] = set()
            for function in contract.functions:
                if function.payable:
                    continue
                for modifier in function.modifiers:
                    if "only" in modifier.name:
                        result_functions.add(function)
                        break

            for result in result_functions:
                result = [
                    result,
                    " should be set to `payable` \n",
                ]
                res = self.generate_result(result)
                results.append(res)
        return results


if __name__ == "__main__":
    unittest.main()
