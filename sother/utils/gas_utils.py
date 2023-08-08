"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from slither.core.compilation_unit import SlitherCompilationUnit
from slither.core.declarations import FunctionContract


class GasUtils:
    @classmethod
    def get_available_functions(
        cls, compilation_unit: "SlitherCompilationUnit"
    ) -> list["FunctionContract"]:
        result_functions: list["FunctionContract"] = []
        for contract in compilation_unit.contracts_derived:
            for function in contract.functions:
                if function.is_constructor_variables:
                    continue
                result_functions.append(function)
        return result_functions


if __name__ == "__main__":
    unittest.main()
