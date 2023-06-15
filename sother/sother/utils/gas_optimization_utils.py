"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from slither.core.compilation_unit import SlitherCompilationUnit
from slither.core.declarations import FunctionContract


class GasOptimizationUtils:
    @classmethod
    def get_for_gas_optimization_functions(
        cls, compilation_unit: "SlitherCompilationUnit"
    ) -> list["FunctionContract"]:
        result_functions: list["FunctionContract"] = []
        for contract in compilation_unit.contracts_derived:
            for function in contract.functions:
                if function.visibility == "external" and (
                    function.view or function.pure
                ):
                    continue
                result_functions.append(function)
        return result_functions


if __name__ == "__main__":
    unittest.main()
