"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.operations.unsafe_tx_origin import UnsafeTxOrigin
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestUnsafeTxOrigin(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UnsafeTxOrigin,
        )
        self.check_detect_results(UnsafeTxOrigin.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
