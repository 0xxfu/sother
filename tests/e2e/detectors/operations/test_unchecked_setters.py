"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.operations.divide_by_constant import DivideByConstant
from sother.detectors.operations.payable_calls import PayableCalls
from sother.detectors.operations.unchecked_setters import UncheckedSetters
from sother.detectors.operations.unsigned_int_compare_zero import UnsignedIntCompareZero
from sother.detectors.operations.unused_return_values import UnusedReturnValues
from sother.detectors.variables.bool_state_variables import BoolStateVariables
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestUncheckedSetters(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UncheckedSetters,
        )
        self.check_detect_results(UncheckedSetters.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()