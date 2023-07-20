"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.operations.use_shifting import DivideByConstant
from sother.detectors.operations.payable_calls import PayableCalls
from sother.detectors.operations.unsafe_casting import UnsafeDowncast, UnsafeDoubleCast
from sother.detectors.operations.unsigned_int_compare_zero import UnsignedIntCompareZero
from sother.detectors.operations.unused_return_values import UnusedReturnValues
from sother.detectors.variables.bool_state_variables import BoolStateVariables
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestUnsafeCasting(DetectorTestCase):
    def test_unsafe_downcast(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UnsafeDowncast,
        )
        self.check_detect_results(UnsafeDowncast.WIKI_TITLE, results)

    def test_unsafe_double_cast(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UnsafeDoubleCast,
        )
        self.check_detect_results(UnsafeDoubleCast.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()