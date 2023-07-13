"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.statements.array_length_in_loop import ArrayLengthInLoop
from sother.detectors.statements.use_delete_statement import UseDeleteStatement
from sother.detectors.statements.used_custom_error import UsedCustomError
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestUseDeleteStatement(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UseDeleteStatement,
        )
        self.check_detect_results(UseDeleteStatement.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
