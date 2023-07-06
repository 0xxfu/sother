"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.variables.bool_state_variables import BoolStateVariables
from sother.detectors.variables.constants_optimization import (
    StringConstants,
    CalculateConstants,
    KeccakConstants,
    KeccakConstantInFunctions,
)
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestConstantsOptimization(DetectorTestCase):
    def test_string_constants(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            StringConstants,
        )
        self.check_detect_results(StringConstants.WIKI_TITLE, results)

    def test_calculate_constants(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            CalculateConstants,
        )
        self.check_detect_results(CalculateConstants.WIKI_TITLE, results)

    def test_keccak_constants(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            KeccakConstants,
        )
        self.check_detect_results(KeccakConstants.WIKI_TITLE, results)

    def test_keccak_constant_in_functions(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            KeccakConstantInFunctions,
        )
        self.check_detect_results(KeccakConstantInFunctions.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
