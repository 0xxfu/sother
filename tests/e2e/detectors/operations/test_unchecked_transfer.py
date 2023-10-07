"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors import UncheckedTransfer, UnsafeTransfer
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestUnsafeCasting(DetectorTestCase):
    def test_unchecked_transfer(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UncheckedTransfer,
        )
        self.check_detect_results(UncheckedTransfer.WIKI_TITLE, results)

    def test_unsafe_transfer(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UnsafeTransfer,
        )
        self.check_detect_results(UnsafeTransfer.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
