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
from solc_select import solc_select

from sother.core.models import OutputResult
from sother.detectors import get_all_detector_wikis


class DetectorTestCase(unittest.TestCase):
    default_solc_version = "0.8.19"

    @classmethod
    def detect(
        cls, sol_file: str, detector: Type[AbstractDetector]
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

    @classmethod
    def check_detect_results(cls, wiki_title: str, results: list[OutputResult]) -> None:
        detector_wikis = get_all_detector_wikis()
        for output_result in results:
            logger.debug(
                f"\nwiki:\n{detector_wikis[output_result.check].wiki_title}\n"
                f"description:\n{output_result.description}\n"
            )
            assert detector_wikis[output_result.check].wiki_title == wiki_title

    def get_test_solidity_filename(self, file):
        return os.path.basename(file).split(".")[0]

    @classmethod
    def set_solc(cls, solc_version: str):  # pylint: disable=too-many-lines
        # hacky hack hack to pick the solc version we want
        env = dict(os.environ)

        if not solc_select.artifact_path(solc_version).exists():
            print("Installing solc version", solc_version)
            solc_select.install_artifacts([solc_version])
        env["SOLC_VERSION"] = solc_version
        os.environ.clear()
        os.environ.update(env)


if __name__ == "__main__":
    unittest.main()
