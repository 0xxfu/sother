"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.pragma.unsafe_floating_pragma import UnsafeFloatingPragma
from sother.detectors.pragma.upgrade_to_latest import UpgradeToLatest
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestUnsafeFloatingPragma(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UnsafeFloatingPragma,
        )
        self.check_detect_results(UnsafeFloatingPragma.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
