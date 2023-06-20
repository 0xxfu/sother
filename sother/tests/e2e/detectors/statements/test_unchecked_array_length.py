"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.statements.array_length_in_loop import ArrayLengthInLoop
from sother.detectors.statements.operator_and_in_require import OperatorAndInRequire
from sother.detectors.statements.unchecked_array_length import UncheckedArrayLength
from sother.detectors.statements.unchecked_in_loop import UncheckedInLoop
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestUncheckedArrayLength(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UncheckedArrayLength,
        )
        self.check_detect_results(UncheckedArrayLength.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
