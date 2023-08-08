"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.operations.unsafe_casting import UnsafeDowncast, UnsafeDoubleCast
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestUnsafeCasting(DetectorTestCase):
    def test_unsafe_downcast(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UnsafeDowncast,
        )
        self.check_detect_results(UnsafeDowncast.WIKI_TITLE, results)

    def test_unsafe_double_cast(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UnsafeDoubleCast,
        )
        self.check_detect_results(UnsafeDoubleCast.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
