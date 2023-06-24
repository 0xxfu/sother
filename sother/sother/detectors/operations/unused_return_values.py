"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from slither.detectors.operations.unused_return_values import (
    UnusedReturnValues as SlitherUnusedReturnValues,
)


# todo
# except ignore returns by statement.
# eg: (a,,c)= functionCalled();
class UnusedReturnValues(SlitherUnusedReturnValues):
    pass


if __name__ == "__main__":
    unittest.main()
