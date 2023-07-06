"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.declarations import FunctionContract
from slither.core.solidity_types import ArrayType, UserDefinedType
from slither.core.variables.local_variable import LocalVariable
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings
from sother.utils.gas_utils import GasUtils


# override by FetchStorageToMemory
class MemoryFromStorage(AbstractDetector):
    ARGUMENT = "memory-from-storage"
    HELP = "Using `storage` instead of `memory` for structs/arrays saves gas"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Using `storage` instead of `memory` for structs/arrays saves gas"
    WIKI_DESCRIPTION = """
When fetching data from a storage location, assigning the data to a `memory` variable causes all fields of the struct/array to be read from storage, which incurs a Gcoldsload (**2100 gas**) for *each* field of the struct/array. If the fields are read from the new memory variable, they incur an additional `MLOAD` rather than a cheap stack read. Instead of declearing the variable with the `memory` keyword, declaring the variable with the `storage` keyword and caching any fields that need to be re-read in stack variables, will be much cheaper, only incuring the Gcoldsload for the fields actually read. The only time it makes sense to read the whole struct/array into a `memory` variable, is if the full struct/array is being returned by the function, is being passed to a function that requires `memory`, or if the array/struct is being read from another `memory` array/struct

More detail see [this.](https://gist.github.com/0xxfu/0ab3b64ba7b342fb88e243d82a763876)
"""

    WIKI_RECOMMENDATION = """
Using `storage` replace `memory` in local variables.
"""

    @classmethod
    def _detect_local_memory(cls, function: FunctionContract) -> set[LocalVariable]:
        result: set[LocalVariable] = set()
        for variable in function.local_variables:
            if isinstance(variable.type, (ArrayType, UserDefinedType)):
                if not variable.is_storage:
                    result.add(variable)
        return result

    def _detect(self) -> List[Output]:
        """
        1. get all struct/mapping states
        2. check function nodes where copy value from state to memory as local variables
        3. return the node list
        """
        results = []

        for function in GasUtils.get_available_functions(self.compilation_unit):
            result_variables = self._detect_local_memory(function)
            for variable in result_variables:
                logger.debug(
                    f"local memory struct/array: {type(variable.type)} {str(variable.expression)}"
                )
                res = self.generate_result(
                    [
                        variable,
                        " should use `storage` instead of `memory` to save gas.\n",
                    ]
                )
                results.append(res)
        return results


if __name__ == "__main__":
    unittest.main()
