"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.pragma.upgrade_to_latest import UpgradeToLatest
from sother.detectors.reentrancy.reentrancy_send_value import ReentrancySendValue
from sother.detectors.reentrancy.reentrancy_transfer import ReentrancyTransfer
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestReentrancyTransfer(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            ReentrancyTransfer,
        )
        self.check_detect_results(ReentrancyTransfer.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
