"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import os
import unittest
from typing import Type

from loguru import logger
from slither import Slither
from slither.detectors.abstract_detector import AbstractDetector

from sother.core.models import OutputResult
from sother.detectors import get_all_detector_wikis


class DetectorTestCase(unittest.TestCase):
    def detect(
        self, sol_file: str, detector: Type[AbstractDetector]
    ) -> list[OutputResult]:
        slither = Slither(sol_file)
        slither.register_detector(detector)
        results = slither.run_detectors()
        output_results = []
        for detector_result in results:
            for detector in detector_result:
                output_result = OutputResult(**detector)
                output_results.append(output_result)
        return output_results

    def check_detect_results(
        self, wiki_title: str, results: list[OutputResult]
    ) -> None:
        detector_wikis = get_all_detector_wikis()
        for output_result in results:
            logger.debug(
                f"\nwiki:\n{detector_wikis[output_result.check].wiki_title}\n"
                f"description:\n{output_result.description}\n"
            )
            assert detector_wikis[output_result.check].wiki_title == wiki_title

    def get_test_solidity_filename(self, file):
        return os.path.basename(file).split(".")[0]


if __name__ == "__main__":
    unittest.main()
