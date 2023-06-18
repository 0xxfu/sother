"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from loguru import logger
from slither.core.solidity_types import UserDefinedType, ArrayType
from slither.core.variables import StateVariable
from slither.core.variables.local_variable import LocalVariable
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
)
from slither.utils.output import Output
from slither.visitors.expression.export_values import ExportValues

from sother.detectors.detector_settings import DetectorSettings
from sother.utils.gas_utils import GasUtils


class FetchStorageToMemory(AbstractDetector):
    ARGUMENT = "fetch-storage-to-memory"
    HELP = "Using `storage` instead of `memory` for structs/arrays saves gas"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Using `storage` instead of `memory` for structs/arrays saves gas"
    WIKI_DESCRIPTION = """When fetching data from a storage location, assigning the data to a `memory` variable causes all fields of the struct/array to be read from storage, which incurs a Gcoldsload (**2100 gas**) for *each* field of the struct/array. If the fields are read from the new memory variable, they incur an additional `MLOAD` rather than a cheap stack read. Instead of declearing the variable with the `memory` keyword, declaring the variable with the `storage` keyword and caching any fields that need to be re-read in stack variables, will be much cheaper, only incuring the Gcoldsload for the fields actually read. The only time it makes sense to read the whole struct/array into a `memory` variable, is if the full struct/array is being returned by the function, is being passed to a function that requires `memory`, or if the array/struct is being read from another `memory` array/struct
    """

    WIKI_RECOMMENDATION = (
        "Fetching data from `storage` directly, don't convert `storage` to `memory`"
    )

    @classmethod
    def _get_array_or_structure(
        cls, variables: list[LocalVariable]
    ) -> list[LocalVariable]:
        results: list[LocalVariable] = []
        for variable in variables:
            if variable.location == "memory":
                if isinstance(variable.type, UserDefinedType) or isinstance(
                    variable.type, ArrayType
                ):
                    results.append(variable)
        return results

    @classmethod
    def _detect_memory_init_from_state(
        cls,
        local_variables: list[LocalVariable],
    ) -> list[(LocalVariable, StateVariable)]:
        results = []

        for local in local_variables:
            if not local.expression:
                continue

            exported_values = ExportValues(local.expression).result()
            for exported_value in exported_values:
                if isinstance(exported_value, StateVariable):
                    results.append((local, exported_value))
        return results

    def _detect(self) -> List[Output]:
        results = []

        for function in GasUtils.get_available_functions(self.compilation_unit):
            if function.is_implemented and function.entry_point:
                memory_variables = self._get_array_or_structure(
                    function.local_variables
                )
                result_variables = self._detect_memory_init_from_state(memory_variables)

                for local, state in result_variables:
                    json = self.generate_result(
                        [
                            "local memory variable ",
                            local,
                            " is initialized from storage: ",
                            state,
                            " should read data from `storage` directly\n",
                        ]
                    )
                    results.append(json)

        return results


if __name__ == "__main__":
    unittest.main()
