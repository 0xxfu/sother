"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.statements.incorrect_deadline import IncorrectDeadline
from sother.detectors.statements.inefficient_new_bytes import InefficientNewBytes
from sother.detectors.statements.memory_from_storage import MemoryFromStorage
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestIncorrectDeadline(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            IncorrectDeadline,
        )
        self.check_detect_results(IncorrectDeadline.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
