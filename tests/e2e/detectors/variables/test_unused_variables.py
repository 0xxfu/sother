"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.variables.unused_variables import (
    UnusedStateVars,
    UnusedNamedReturnVariables,
    UnusedParameter,
)
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestUnusedState(DetectorTestCase):
    def test_unused_state_variables(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UnusedStateVars,
        )
        self.check_detect_results(UnusedStateVars.WIKI_TITLE, results)

    def test_unused_named_return_variables(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UnusedNamedReturnVariables,
        )
        self.check_detect_results(UnusedNamedReturnVariables.WIKI_TITLE, results)

    def test_unused_parameter(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UnusedParameter,
        )
        self.check_detect_results(UnusedParameter.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
