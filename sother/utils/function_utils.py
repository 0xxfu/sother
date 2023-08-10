"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-08
"""
import unittest

from slither.core.declarations import Function


class FunctionUtils:
    @classmethod
    def is_entry_point_function(cls, function: Function) -> bool:
        return (
            function.visibility in ["public", "external"]
            and not function.is_shadowed
            or function.is_fallback
        )


if __name__ == "__main__":
    unittest.main()
