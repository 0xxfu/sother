"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.statements.operator_and_in_require import OperatorAndInRequire
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestOperatorAndInRequire(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            OperatorAndInRequire,
        )
        self.check_detect_results(OperatorAndInRequire.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
