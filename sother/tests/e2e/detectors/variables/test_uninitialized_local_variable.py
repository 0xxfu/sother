"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.variables.uninitialized_local_variables import (
    UninitializedLocalVars,
)
from sother.detectors.variables.unused_state_variables import UnusedStateVariables
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestUninitializedLocalVars(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UninitializedLocalVars,
        )
        self.check_detect_results(UninitializedLocalVars.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
