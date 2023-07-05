"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest
from typing import List

from loguru import logger
from slither.core.variables import StateVariable
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class StringConstants(AbstractDetector):
    ARGUMENT = "string-constants"
    HELP = "`Bytes` constants are more efficient than `string` constants"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "`Bytes` constants are more efficient than `string` constants"

    WIKI_DESCRIPTION = """
From the [Solidity doc](https://docs.soliditylang.org/en/develop/types.html#arrays):
> If you can limit the length to a certain number of bytes, 
> always use one of the value types `bytes1` to `bytes32` because they are much cheaper.

[Why do Solidity examples use bytes32 type instead of string?](https://ethereum.stackexchange.com/questions/3795/why-do-solidity-examples-use-bytes32-type-instead-of-string)

`bytes32` uses less gas because it fits in a single word of the EVM, 
and `string` is a dynamically sized-type which has current limitations in Solidity 
(such as can’t be returned from a function to a contract).

If data can fit into 32 bytes, then you should use `bytes32` datatype rather than `bytes` or `strings`
 as it is cheaper in solidity. 
 Basically, any fixed size variable in solidity is cheaper than variable size. 
 That will save gas on the contract.
"""
    WIKI_RECOMMENDATION = """
Replace `string` constant with `bytes(1..32)` constant.
"""

    @classmethod
    def _is_string_constant(cls, state: StateVariable) -> bool:
        if state.is_constant and str(state.type) == "string":
            return True
        return False

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for state in contract.state_variables_declared:
                if self._is_string_constant(state):
                    json = self.generate_result(
                        [state, " should use `bytes(1..31)` instead of `string`.\n"]
                    )
                    results.append(json)
        return results


if __name__ == "__main__":
    unittest.main()
