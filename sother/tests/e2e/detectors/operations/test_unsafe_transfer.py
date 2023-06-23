"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.operations.divide_by_constant import DivideByConstant
from sother.detectors.operations.payable_calls import PayableCalls
from sother.detectors.operations.unsafe_transfer import UnsafeTransferErc721
from sother.detectors.variables.bool_state_variables import BoolStateVariables
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestUnsafeTransferErc721(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UnsafeTransferErc721,
        )
        self.check_detect_results(UnsafeTransferErc721.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
