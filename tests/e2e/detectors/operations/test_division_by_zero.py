"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.operations.assignment_left_operation import (
    AssignmentLeftOperation,
)
from sother.detectors.operations.division_by_zero import DivisionByZero
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestDivisionByZero(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            DivisionByZero,
        )
        self.check_detect_results(DivisionByZero.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
