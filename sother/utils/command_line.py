"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-08
"""
import unittest
from collections import defaultdict
from typing import Type

from slither.detectors import all_detectors as slither_all_detectors
from slither.detectors.abstract_detector import (
    AbstractDetector,
    classification_txt,
    DetectorClassification,
)
from slither.utils.colors import blue, green

from sother.detectors import get_all_detectors, get_detectors
from sother.detectors.falcon.detectors import all_detectors as falcon_all_detectors
from sother.utils.detector_utils import DetectorUtils


def output_detector_stats(detectors: list[Type[AbstractDetector]]) -> None:
    impact_detectors: dict[
        DetectorClassification, list[Type[AbstractDetector]]
    ] = defaultdict(list)
    for item in detectors:
        impact_detectors[item.IMPACT].append(item)
    impacts = sorted(impact_detectors.keys(), key=lambda x: x.value)
    for item in impacts:
        print(f"{classification_txt[item]}: {len(impact_detectors[item])}")
    print(green(f"Total: {len(detectors)}"))


def output_stats():
    print(blue("------ All ------"))
    detectors = get_all_detectors()
    output_detector_stats(detectors)

    print(blue("\n------ Sother ------"))
    detectors = get_detectors()
    output_detector_stats(detectors)

    print(blue("\n------ Slither ------"))
    output_detector_stats(DetectorUtils.get_detectors_from_file(slither_all_detectors))

    print(blue("\n------ Falcon ------"))
    output_detector_stats(DetectorUtils.get_detectors_from_file(falcon_all_detectors))

    print("\n")


class CommandLineTestCase(unittest.TestCase):
    def test_stat_detectors(self):
        output_stats()


if __name__ == "__main__":
    unittest.main()
