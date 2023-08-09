"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-08
"""
import unittest
from collections import defaultdict
from typing import Type

from slither.detectors.abstract_detector import (
    AbstractDetector,
    classification_txt,
    DetectorClassification,
)
from slither.utils.colors import blue

from sother.detectors import get_all_detectors, get_detectors


def output_detector_stats(detectors: list[Type[AbstractDetector]]) -> None:
    impact_detectors: dict[
        DetectorClassification, list[Type[AbstractDetector]]
    ] = defaultdict(list)
    for item in detectors:
        impact_detectors[item.IMPACT].append(item)
    impacts = sorted(impact_detectors.keys(), key=lambda x: x.value)
    for item in impacts:
        print(f"{classification_txt[item]}: {len(impact_detectors[item])}")
    print(f"Total: {len(detectors)}")


class CommandLineTestCase(unittest.TestCase):
    def test_stat_detectors(self):
        print(blue("------ All ------"))
        detectors = get_all_detectors()
        output_detector_stats(detectors)

        print(blue("------ Sother ------"))
        detectors = get_detectors()
        output_detector_stats(detectors)


if __name__ == "__main__":
    unittest.main()
