"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.operations.use_shifting import DivideByConstant, MulPowerTwo
from sother.detectors.variables.bool_state_variables import BoolStateVariables
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestUseShifting(DetectorTestCase):
    def test_divide_by_constant(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            DivideByConstant,
        )
        self.check_detect_results(DivideByConstant.WIKI_TITLE, results)

    def test_mul_power_two(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            MulPowerTwo,
        )
        self.check_detect_results(MulPowerTwo.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
