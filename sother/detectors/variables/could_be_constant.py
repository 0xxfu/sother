"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from slither.detectors.variables.could_be_constant import (
    CouldBeConstant as SlitherCouldBeConstant,
)


class CouldBeConstant(SlitherCouldBeConstant):
    pass


if __name__ == "__main__":
    unittest.main()
