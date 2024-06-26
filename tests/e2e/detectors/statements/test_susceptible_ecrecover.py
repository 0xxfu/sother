"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.statements.susceptible_ecrecover import (
    SusceptibleEcrecover,
    UncheckedEcrecover,
)
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestSusceptibleEcrecover(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            SusceptibleEcrecover,
        )
        self.check_detect_results(SusceptibleEcrecover.WIKI_TITLE, results)

    def test_unchecke_decrecover(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UncheckedEcrecover,
        )
        self.check_detect_results(UncheckedEcrecover.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
