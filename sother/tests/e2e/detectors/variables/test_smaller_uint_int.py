"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import os
import unittest

from sother.core.models import OutputResult
from sother.detectors.variables.smaller_uint_int import SmallerUintInt
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestSmallerUintInt(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            SmallerUintInt,
        )
        self.check_detect_results(SmallerUintInt.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
