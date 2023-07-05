"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.variables.bool_state_variables import BoolStateVariables
from sother.detectors.variables.string_constants import StringConstants
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestBytesConstants(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            StringConstants,
        )
        self.check_detect_results(StringConstants.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
