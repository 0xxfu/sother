"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult

from sother.detectors.operations.zero_address_optimization import (
    ZeroAddressOptimization,
)

from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestZeroAddressOptimization(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            ZeroAddressOptimization,
        )
        self.check_detect_results(ZeroAddressOptimization.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
