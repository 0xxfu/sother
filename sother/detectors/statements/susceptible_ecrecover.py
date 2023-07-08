"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest
from typing import List

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.declarations import FunctionContract
from slither.detectors.abstract_detector import DetectorClassification, AbstractDetector
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class SusceptibleEcrecover(AbstractDetector):
    ARGUMENT = "susceptible-ecrecover"
    HELP = "Direct usage of `ecrecover` allows signature malleability"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Direct usage of `ecrecover` allows signature malleability"
    WIKI_DESCRIPTION = """
The `ecrecover` function is used to verify and execute Meta transactions. 
The built-in EVM precompile `ecrecover` is susceptible to signature malleability 
(because of non-unique s and v values) which could lead to replay attacks 
(references: https://swcregistry.io/docs/SWC-117, https://swcregistry.io/docs/SWC-121 and https://medium.com/cryptronics/signature-replay-vulnerabilities-in-smart-contracts-3b6f7596df57).

While this is not exploitable for replay attacks in the current implementation because of the use of nonces, this may become a vulnerability if used elsewhere.
"""
    WIKI_EXPLOIT_SCENARIO = """ """

    WIKI_RECOMMENDATION = """
Consider using [OpenZeppelin’s ECDSA library](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/ECDSA.sol) 
(which prevents this malleability) instead of the built-in function.
"""

    @classmethod
    def _detect_use_ecrecover(cls, function: FunctionContract) -> set[Node]:
        result_nodes: set[Node] = set()
        for node in function.nodes:
            for ir in node.irs:
                if "ecrecover(bytes32,uint8,bytes32,bytes32)" in str(ir.expression):
                    result_nodes.add(node)
        return result_nodes

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for function in contract.functions:
                result_nodes: set[Node] = self._detect_use_ecrecover(function)
                for node in result_nodes:
                    res = self.generate_result(
                        [
                            node,
                            " should OpenZeppelin’s ECDSA instead of the built-in function.\n",
                        ]
                    )
                    results.append(res)
        return results


class UncheckedEcrecover(AbstractDetector):
    ARGUMENT = "unchecked-ecrecover"
    HELP = "return value of 0 from `ecrecover` not checked"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "return value of 0 from `ecrecover` not checked"
    WIKI_DESCRIPTION = """
The solidity function `ecrecover` is used, however the error result of 0 is not checked for.
See documentation:
https://docs.soliditylang.org/en/latest/units-and-global-variables.html#mathematical-and-cryptographic-functions
> recover the address associated with the public key from elliptic curve signature or return zero on error.  
"""
    WIKI_EXPLOIT_SCENARIO = """ """

    WIKI_RECOMMENDATION = """
Verify that the result from `ecrecover` isn't `0`
"""

    @classmethod
    def _detect_unchcked_ecrecover(cls, function: FunctionContract) -> set[Node]:
        result_nodes: set[Node] = set()
        for node in function.nodes:
            for ir in node.irs:
                if "ecrecover(bytes32,uint8,bytes32,bytes32)" in str(ir.expression):
                    # todo detect unchecked result
                    pass
        return result_nodes

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for function in contract.functions:
                result_nodes: set[Node] = self._detect_unchcked_ecrecover(function)
                for node in result_nodes:
                    res = self.generate_result(
                        [
                            node,
                            " should check the result from `ecrecover` isn't `0`.\n",
                        ]
                    )
                    results.append(res)
        return results


if __name__ == "__main__":
    unittest.main()
