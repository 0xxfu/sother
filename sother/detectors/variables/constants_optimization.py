"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest
from typing import List, Any

from loguru import logger
from slither.core.expressions import BinaryOperation, CallExpression
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


class CalculateConstants(AbstractDetector):
    ARGUMENT = "calculate-constants"
    HELP = "Do not calculate constants"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Do not calculate constants"

    WIKI_DESCRIPTION = """
Due to how constant variables are implemented (replacements at compile-time), 
an expression assigned to a constant variable is recomputed each time that the variable is used, 
which wastes some gas.

See: [ethereum/solidity#9232](https://github.com/ethereum/solidity/issues/9232):
> each usage of a "constant" costs ~100gas more on each access (it is still a little better than storing the result in storage, but not much..)

> since these are not real constants, they can't be referenced from a real constant environment (e.g. from assembly, or from another library )

"""
    WIKI_RECOMMENDATION = """
Pre-calculate the results(hardcode) instead of calculation in runtime.
"""

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for state in contract.state_variables_declared:
                if self._is_calculate_constant(state):
                    json = self.generate_result(
                        [state, " should use hardcode instead of calculation.\n"]
                    )
                    results.append(json)
        return results

    @classmethod
    def _is_calculate_constant(cls, state: StateVariable) -> bool:
        if state.is_constant and isinstance(state.expression, BinaryOperation):
            return True
        return False


class KeccakConstants(AbstractDetector):
    ARGUMENT = "keccak-constants"
    HELP = "Instead of calculating a state variable with `keccak256()`/`abi.encode**()` every time the contract is made pre calculate them before and only give the result to a constant"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Instead of calculating a state variable with `keccak256()`/`abi.encode**()` every time the contract is made pre calculate them before and only give the result to a constant"

    WIKI_DESCRIPTION = """
Due to how constant variables are implemented (replacements at compile-time), 
an expression assigned to a constant variable is recomputed each time that the variable is used, 
which wastes some gas.

See: [ethereum/solidity#9232](https://github.com/ethereum/solidity/issues/9232):
> each usage of a "constant" costs ~100gas more on each access (it is still a little better than storing the result in storage, but not much..)

> since these are not real constants, they can't be referenced from a real constant environment (e.g. from assembly, or from another library )

"""
    WIKI_RECOMMENDATION = """
Pre-calculate the results(hardcode) instead of calculate `keccak256`/`abi.encode**` in runtime.
"""

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for state in contract.state_variables_declared:
                if self._is_keccak_constant(state):
                    json = self.generate_result(
                        [
                            state,
                            " should use pre-calculate results instead of calculation in runtime.\n",
                        ]
                    )
                    results.append(json)
        return results

    @classmethod
    def _is_keccak_constant(cls, state: StateVariable) -> bool:
        if (
            state.is_constant
            and isinstance(state.expression, CallExpression)
            and any(
                [
                    "keccak256" in str(state.expression),
                    "abi.encode" in str(state.expression),
                ]
            )
        ):
            return True
        return False


if __name__ == "__main__":
    unittest.main()
