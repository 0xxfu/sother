"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from slither.core.expressions import BinaryOperation, CallExpression

"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.analyses.data_dependency.data_dependency import is_dependent
from slither.core.declarations import FunctionContract, SolidityVariableComposed
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.slithir.operations import Binary, InternalCall
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class MissingSupportsInterface(AbstractDetector):
    ARGUMENT = "missing-supports-interface"
    HELP = "Missing `supportsInterface` functions"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki
    WIKI_TITLE = "Missing `supportsInterface` functions"

    WIKI_DESCRIPTION = """
According to [EIP-165](https://eips.ethereum.org/EIPS/eip-165), 
a contract’s implementation of the supportsInterface function
should return true for the interfaces that the contract supports. 
"""
    WIKI_EXPLOIT_SCENARIO = """ """

    WIKI_RECOMMENDATION = """
Short term, add supportsInterface functions to all contracts that implement a well-known interface. 
Doing so will help to ensure that contracts can interact with external contracts.

Long term, add tests to ensure that each contract’s supportsInterface function returns
true for the interfaces that the contract supports and false for some subset of the
interfaces that the contract does not support. Doing so will help to ensure that the
supportsInterface functions work correctly.
"""

    def _detect(self) -> list[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            if contract.is_possible_erc721():
                if not any(
                    [
                        function.signature_str
                        == "supportsInterface(bytes4) returns(bool)"
                        for function in contract.functions
                    ]
                ):
                    res = self.generate_result(
                        [
                            contract,
                            " missing `supportsInterface()`.\n",
                        ]
                    )
                    results.append(res)

        return results


if __name__ == "__main__":
    unittest.main()
