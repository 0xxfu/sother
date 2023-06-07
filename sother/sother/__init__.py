import inspect
import sys
from typing import Tuple, List, Type

from slither.__main__ import get_detectors_and_printers, main_impl

from slither.detectors.abstract_detector import AbstractDetector
from slither.printers.abstract_printer import AbstractPrinter

from sother.detectors import all_detectors
from sother.printers import all_printers


def get_plugin_detectors_and_printers() -> (
    Tuple[
        list[Type[AbstractDetector]],
        list[Type[AbstractPrinter]],
    ]
):
    detectors_ = [getattr(all_detectors, name) for name in dir(all_detectors)]
    detectors = [
        d for d in detectors_ if inspect.isclass(d) and issubclass(d, AbstractDetector)
    ]

    printers_ = [getattr(all_printers, name) for name in dir(all_printers)]
    printers = [
        p for p in printers_ if inspect.isclass(p) and issubclass(p, AbstractPrinter)
    ]
    return detectors, printers


def main() -> Tuple[List[Type[AbstractDetector]], List[Type[AbstractPrinter]]]:
    plugin_detectors, plugin_printers = get_plugin_detectors_and_printers()
    # Codebase with complex domninators can lead to a lot of SSA recursive call
    sys.setrecursionlimit(1500)

    detectors, printers = get_detectors_and_printers()
    detectors += plugin_detectors
    printers += plugin_printers

    main_impl(all_detector_classes=detectors, all_printer_classes=printers)
    return detectors, printers
