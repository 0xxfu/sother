"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest
from typing import List

from slither.detectors.functions.external_function import ExternalFunction as SlitherExternalFunction
from slither.utils.output import Output


class ExternalFunction(SlitherExternalFunction):
    VULNERABLE_SOLC_VERSIONS = None




if __name__ == "__main__":
    unittest.main()
