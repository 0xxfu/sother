"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.erc.erc721.missing_supports_interface import (
    MissingSupportsInterface,
)
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestMissingSupportsInterface(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            MissingSupportsInterface,
        )
        self.check_detect_results(MissingSupportsInterface.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
