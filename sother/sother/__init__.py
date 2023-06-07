import sys
from typing import Tuple, List, Type

from slither.__main__ import get_detectors_and_printers, main_impl

from sother.detectors.example import Example

from slither.detectors.abstract_detector import AbstractDetector
from slither.printers.abstract_printer import AbstractPrinter


def main() -> Tuple[List[Type[AbstractDetector]], List[Type[AbstractPrinter]]]:
    plugin_detectors = [Example]
    plugin_printers: List[Type[AbstractPrinter]] = []
    # Codebase with complex domninators can lead to a lot of SSA recursive call
    sys.setrecursionlimit(1500)

    detectors, printers = get_detectors_and_printers()
    detectors = detectors + plugin_detectors
    printers = printers + plugin_printers

    main_impl(all_detector_classes=detectors, all_printer_classes=printers)
    return plugin_detectors, plugin_printers
