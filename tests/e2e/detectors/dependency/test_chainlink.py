"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.dependency.chainlink import (
    DeprecatedChainLink,
    UncheckedChainlinkStaleness,
    IgnoredChainlinkReturns,
    UncheckedChainlinkRound,
)

from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestChainLink(DetectorTestCase):
    def test_deprecated_chainlink(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            DeprecatedChainLink,
        )
        self.check_detect_results(DeprecatedChainLink.WIKI_TITLE, results)

    def test_ignored_chainlink_returns(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            IgnoredChainlinkReturns,
        )
        self.check_detect_results(IgnoredChainlinkReturns.WIKI_TITLE, results)

    def test_unchecked_chainlink_staleness(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UncheckedChainlinkStaleness,
        )
        self.check_detect_results(UncheckedChainlinkStaleness.WIKI_TITLE, results)

    def test_unchecked_chainlink_round(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UncheckedChainlinkRound,
        )
        self.check_detect_results(UncheckedChainlinkRound.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
