"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult

from sother.detectors.variables.uninitialized_state_variables import (
    UninitializedStateVarsDetection,
)
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestUninitializedStateVarsDetection(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UninitializedStateVarsDetection,
        )
        self.check_detect_results(UninitializedStateVarsDetection.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
