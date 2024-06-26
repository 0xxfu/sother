"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.statements.unchecked_in_loop import UncheckedInLoop
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestUncheckedInLoop(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UncheckedInLoop,
        )
        self.check_detect_results(UncheckedInLoop.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
