"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.source.open_todos import OpenTodos
from sother.detectors.source.safe_math_lib import SafeMathLib
from sother.detectors.statements.array_length_in_loop import ArrayLengthInLoop
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestOpenTodos(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            OpenTodos,
        )
        self.check_detect_results(OpenTodos.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
