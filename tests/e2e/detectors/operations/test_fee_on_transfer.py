"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.operations.use_shifting import DivideByConstant
from sother.detectors.operations.fee_on_transfer import FeeOnTransfer
from sother.detectors.operations.payable_calls import PayableCalls
from sother.detectors.variables.bool_state_variables import BoolStateVariables
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestFeeOnTransfer(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            FeeOnTransfer,
        )
        self.check_detect_results(FeeOnTransfer.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
