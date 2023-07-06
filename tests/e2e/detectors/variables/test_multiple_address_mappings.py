"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import os
import unittest

from sother.core.models import OutputResult
from sother.detectors.variables.multiple_address_mappings import MultipleAddressMappings
from sother.detectors.variables.public_to_private_constant import (
    PublicToPrivateConstant,
)
from sother.detectors.variables.smaller_uint_int import SmallerUintInt
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestMultipleAddressMappings(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            MultipleAddressMappings,
        )
        self.check_detect_results(MultipleAddressMappings.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
