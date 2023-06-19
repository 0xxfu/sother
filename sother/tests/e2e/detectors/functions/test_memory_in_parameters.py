"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.functions.internal_function_to_inline import (
    InternalFunctionToInline,
)
from sother.detectors.functions.memory_in_parameters import MemoryInParameters
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestInternalFunctionToInline(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            MemoryInParameters,
        )
        wiki = MemoryInParameters.WIKI_TITLE
        self.check_detect_results(wiki, results)


if __name__ == "__main__":
    unittest.main()
