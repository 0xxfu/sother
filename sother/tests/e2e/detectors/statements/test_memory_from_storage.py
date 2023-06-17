"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.statements.assignment_left_operation import (
    AssignmentLeftOperation,
)
from sother.detectors.statements.memory_from_storage import MemoryFromStorage
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestMemoryFromStorage(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            MemoryFromStorage,
        )
        self.check_detect_results(MemoryFromStorage.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
