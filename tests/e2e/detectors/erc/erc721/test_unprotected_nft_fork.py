"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.erc.erc721.unprotected_nft_fork import UnprotectedNFTFork
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestUnprotectedNFTFork(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UnprotectedNFTFork,
        )
        self.check_detect_results(UnprotectedNFTFork.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
