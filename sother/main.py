"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import importlib.metadata
import os
import sys
import unittest
from typing import Type, Tuple, List

import click
from loguru import logger
from slither.__main__ import main_impl
from slither.detectors.abstract_detector import AbstractDetector
from slither.printers.abstract_printer import AbstractPrinter
from slither.utils.colors import blue
from slither.utils.command_line import output_detectors

from sother.detectors import get_all_detectors, get_detectors
from sother.printers import get_all_printers
from sother.utils.command_line import output_detector_stats


def get_detectors_and_printers() -> (
    Tuple[
        list[Type[AbstractDetector]],
        list[Type[AbstractPrinter]],
    ]
):
    return get_all_detectors(), get_all_printers()


def guru_logger():
    log_level = os.environ.get("LOGURU_LEVEL") or os.environ.get("loguru_level")
    if not log_level:
        logger.remove(0)
        logger.add(sys.stdout, level="INFO")


def start() -> Tuple[List[Type[AbstractDetector]], List[Type[AbstractPrinter]]]:
    guru_logger()
    # Codebase with complex domninators can lead to a lot of SSA recursive call
    sys.setrecursionlimit(1500)
    detectors, printers = get_detectors_and_printers()

    main_impl(all_detector_classes=detectors, all_printer_classes=printers)
    return detectors, printers


@click.group()
def cli():
    pass


@cli.command()
def detector_stats():
    print(blue("------ All ------"))
    detectors = get_all_detectors()
    output_detector_stats(detectors)

    print(blue("------ Sother ------"))
    detectors = get_detectors()
    output_detector_stats(detectors)


@cli.command()
def list_detector():
    detectors = get_all_detectors()
    output_detectors(detectors)


@cli.command()
def version():
    __version__ = importlib.metadata.version(__package__ or __name__)
    print(f"version: {__version__}")


class DetectorTestCase(unittest.TestCase):
    def test_get_detectors(self):
        detectors = get_all_detectors()
        for item in detectors:
            print(item.ARGUMENT)
        print(f"total detectors: {len(detectors)}")

    def test_get_printers(self):
        printers = get_all_printers()
        for item in printers:
            print(item.ARGUMENT)
        print(f"total printers: {len(printers)}")


if __name__ == "__main__":
    unittest.main()
