"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.statements.array_length_in_loop import ArrayLengthInLoop
from sother.detectors.statements.used_custom_error import UsedCustomError
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestUsedCustomError(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UsedCustomError,
        )
        self.check_detect_results(UsedCustomError.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
