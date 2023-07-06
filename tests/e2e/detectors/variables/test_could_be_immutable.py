"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from slither import Slither

from sother.core.models import OutputResult
from sother.detectors import get_all_detector_wikis
from sother.detectors.variables.could_be_immutable import CouldBeImmutable
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestCouldBeImmutable(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            CouldBeImmutable,
        )
        self.check_detect_results(CouldBeImmutable.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
