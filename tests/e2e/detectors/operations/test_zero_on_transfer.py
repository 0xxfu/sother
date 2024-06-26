"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult

from sother.detectors.operations.zero_on_transfer import ZeroCheckWithTransfer
from sother.detectors.variables.bool_state_variables import BoolStateVariables
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestFeeOnTransfer(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            ZeroCheckWithTransfer,
        )
        self.check_detect_results(ZeroCheckWithTransfer.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
