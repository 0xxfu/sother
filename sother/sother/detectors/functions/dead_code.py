"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from slither.detectors.abstract_detector import DetectorClassification
from slither.detectors.functions.dead_code import DeadCode as SlitherDeadCode

from sother.detectors.detector_settings import DetectorSettings


class DeadCode(SlitherDeadCode):
    ARGUMENT = "dead-code"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki
    WIKI_TITLE = (
        "Dead-code: functions not used should be removed to save deployment gas"
    )
    WIKI_EXPLOIT_SCENARIO = ""


if __name__ == "__main__":
    unittest.main()
