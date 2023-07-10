"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import os
import unittest

from loguru import logger

from sother.core.models import OutputResult
from sother.detectors.pragma.unsafe_assembly import UnsafeAssembly
from sother.detectors.pragma.unsafe_floating_pragma import UnsafeFloatingPragma
from sother.detectors.pragma.upgrade_to_latest import UpgradeToLatest
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestUnsafeAssembly(DetectorTestCase):
    def test_unsafe_assembly(self):
        folder_path = f"{self.get_test_solidity_filename(__file__)}/"
        versions = [
            os.path.splitext(file)[0]
            for file in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, file))
        ]
        for version in versions:
            self.test_detect(version)

    def test_detect(self, version: str):
        logger.debug(f"test solc version: {version}")
        self.set_solc(version)
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}/{version}.sol",
            UnsafeAssembly,
        )
        self.check_detect_results(UnsafeAssembly.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
