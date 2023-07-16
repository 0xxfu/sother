"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.dependency.chainlink import DeprecatedChainLink
from sother.detectors.dependency.unsafe_solmate_transfer_lib import (
    UnsafeSolmateTransferLib,
)
from sother.detectors.functions.cache_call_function_result import (
    CacheCallFunctionResult,
)
from sother.detectors.functions.internal_function_to_inline import (
    InternalFunctionToInline,
)
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestChainLink(DetectorTestCase):
    def test_deprecated_chainlink(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            DeprecatedChainLink,
        )
        self.check_detect_results(DeprecatedChainLink.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
