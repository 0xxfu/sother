"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.erc.erc20.deprecated_safe_approve import DeprecatedSafeApprove
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestDeprecatedSafeApprove(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            DeprecatedSafeApprove,
        )
        self.check_detect_results(DeprecatedSafeApprove.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
