"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.pragma.upgrade_to_latest import UpgradeToLatest
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestUpgradeToLatest(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            "test_upgrade_to_latest.sol", UpgradeToLatest
        )
        wiki = UpgradeToLatest.WIKI_TITLE
        self.check_detect_results(wiki, results)


if __name__ == "__main__":
    unittest.main()
