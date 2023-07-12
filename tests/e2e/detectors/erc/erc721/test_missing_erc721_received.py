"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.erc.erc721.missing_erc721_received import (
    MissingErc721Received,
    UncheckedErc721Received,
)

from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestMissingErc721Received(DetectorTestCase):
    def test_missing_erc721_received(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            MissingErc721Received,
        )
        self.check_detect_results(MissingErc721Received.WIKI_TITLE, results)

    def test_unchecked_erc721_received(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UncheckedErc721Received,
        )
        self.check_detect_results(UncheckedErc721Received.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
