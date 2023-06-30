"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from loguru import logger
from slither.core.declarations import FunctionContract
from slither.core.solidity_types import ArrayType, UserDefinedType, MappingType
from slither.core.variables.local_variable import LocalVariable
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings
from sother.utils.gas_utils import GasUtils


# todo only detect in entrypoint function
class MemoryInParameters(AbstractDetector):
    ARGUMENT = "memory-in-parameters"
    HELP = "Use `calldata` instead of `memory` for function parameters"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Use `calldata` instead of `memory` for function parameters"
    WIKI_DESCRIPTION = """
On external functions, when using the `memory` keyword with a function argument, what's happening is a `memory` acts as an intermediate.

When the function gets called externally, the array values are kept in `calldata` and copied to memory during ABI decoding (using the opcode `calldataload` and `mstore`). 
And during the for loop, the values in the array are accessed in memory using a `mload`. That is inefficient. Reading directly from `calldata` using `calldataload` instead of going via `memory` saves the gas from the intermediate memory operations that carry the values.

More detail see [this](https://ethereum.stackexchange.com/questions/74442/when-should-i-use-calldata-and-when-should-i-use-memory)
"""

    WIKI_RECOMMENDATION = "Use `calldata` instead of `memory` for external functions where the function argument is read-only."

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for function in contract.functions_entry_points:
                result_variables = self._detect_memory_variables(function)
                if result_variables and len(result_variables) > 0:
                    logger.debug(
                        f"memory variables: {[item.name for item in result_variables]}"
                    )
                    result = [
                        function,
                        " read-only `memory` parameters below should be changed to `calldata` :\n",
                    ]
                    for item in result_variables:
                        result += ["\t- ", item, "\n"]
                    res = self.generate_result(result)
                    results.append(res)

        return results

    @classmethod
    def _detect_memory_variables(
        cls, function: FunctionContract
    ) -> list[LocalVariable]:
        memory_variables: list[LocalVariable] = list()
        variables_written = function.variables_written
        for param in function.parameters:
            if (
                param.location == "memory"
                and param not in variables_written
                and isinstance(param.type, (ArrayType, UserDefinedType, MappingType))
            ):
                memory_variables.append(param)
        return memory_variables


if __name__ == "__main__":
    unittest.main()
