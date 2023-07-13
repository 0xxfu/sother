"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.operations.use_selfbalance import (
    UseSelfBalance,
    UseAssemblyBalance,
)

from sother.detectors.operations.zero_address_optimization import (
    ZeroAddressOptimization,
)

from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestUseSelfBalance(DetectorTestCase):
    def test_use_self_balance(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UseSelfBalance,
        )
        self.check_detect_results(UseSelfBalance.WIKI_TITLE, results)

    def test_use_assembly_balance(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            UseAssemblyBalance,
        )
        self.check_detect_results(UseAssemblyBalance.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
