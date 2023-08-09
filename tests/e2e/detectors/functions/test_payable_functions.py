"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.functions.payable_functions import (
    PayableConstructor,
    PayableFunction,
)
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestPayableFunctions(DetectorTestCase):
    def test_payable_constructor(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            PayableConstructor,
        )
        wiki = PayableConstructor.WIKI_TITLE
        self.check_detect_results(wiki, results)

    def test_payable_function(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            PayableFunction,
        )
        wiki = PayableFunction.WIKI_TITLE
        self.check_detect_results(wiki, results)


if __name__ == "__main__":
    unittest.main()
