"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.statements.inefficient_new_bytes import InefficientNewBytes
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestInefficientNewBytes(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            InefficientNewBytes,
        )
        self.check_detect_results(InefficientNewBytes.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
