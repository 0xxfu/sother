"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.erc.erc20.revert_on_total_supply import RevertOnTotalSupply
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestRevertOnTotalSupply(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            RevertOnTotalSupply,
        )
        self.check_detect_results(RevertOnTotalSupply.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
