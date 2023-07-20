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
    UnusedLocalVar,
    UnusedStruct,
    UnusedError,
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

    def test_unused_local_var(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UnusedLocalVar,
        )
        self.check_detect_results(UnusedLocalVar.WIKI_TITLE, results)

    def test_unused_struct(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UnusedStruct,
        )
        self.check_detect_results(UnusedStruct.WIKI_TITLE, results)

    def test_unused_error(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UnusedError,
        )
        self.check_detect_results(UnusedError.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
