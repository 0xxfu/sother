"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import sys
import unittest
from typing import Type, Tuple, List

from slither.__main__ import main_impl
from slither.detectors.abstract_detector import AbstractDetector
from slither.printers.abstract_printer import AbstractPrinter

from sother.detectors import get_all_detectors
from sother.printers import get_all_printers


def get_detectors_and_printers() -> (
    Tuple[
        list[Type[AbstractDetector]],
        list[Type[AbstractPrinter]],
    ]
):
    return get_all_detectors(), get_all_printers()


def start() -> (
    Tuple[List[Type[AbstractDetector]], List[Type[AbstractPrinter]]]
):
    # Codebase with complex domninators can lead to a lot of SSA recursive call
    sys.setrecursionlimit(1500)
    detectors, printers = get_detectors_and_printers()

    main_impl(all_detector_classes=detectors, all_printer_classes=printers)
    return detectors, printers


class DetectorTestCase(unittest.TestCase):
    def test_get_detectors(self):
        for item in get_all_detectors():
            print(item.ARGUMENT)


if __name__ == "__main__":
    unittest.main()
