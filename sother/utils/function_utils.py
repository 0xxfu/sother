"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-08
"""
import unittest

from slither.analyses.data_dependency.data_dependency import is_dependent
from slither.core.declarations import Function
from slither.core.variables.local_variable import LocalVariable


class FunctionUtils:
    @classmethod
    def is_entry_point_function(cls, function: Function) -> bool:
        return (
            function.visibility in ["public", "external"]
            and not function.is_shadowed
            or function.is_fallback
        )

    @classmethod
    def is_local_var_dependent_param(
        cls, local_var: LocalVariable, function: Function
    ) -> bool:
        return isinstance(local_var, LocalVariable) and any(
            [is_dependent(local_var, param, function) for param in function.parameters]
        )


if __name__ == "__main__":
    unittest.main()
