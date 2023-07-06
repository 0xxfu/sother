"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List, Tuple

from loguru import logger
from slither.core.declarations import Contract, Function
from slither.core.solidity_types import ElementaryType, UserDefinedType
from slither.core.variables import Variable
from slither.detectors.variables.uninitialized_state_variables import (
    UninitializedStateVarsDetection as SlitherUninitializedStateVarsDetection,
)


class UninitializedStateVarsDetection(SlitherUninitializedStateVarsDetection):
    def _detect_uninitialized(
        self, contract: Contract
    ) -> List[Tuple[Variable, List[Function]]]:
        written_variables = self._written_variables(contract)
        written_variables += self._written_variables_in_proxy(contract)
        read_variables = self._read_variables(contract)

        return [
            (variable, contract.get_functions_reading_from_variable(variable))
            for variable in contract.state_variables
            if variable not in written_variables
            and not variable.expression
            and variable in read_variables
            and isinstance(variable.type, (ElementaryType, UserDefinedType))
            and str(variable.type) in ["address", "IERC20"]
        ]


if __name__ == "__main__":
    unittest.main()
