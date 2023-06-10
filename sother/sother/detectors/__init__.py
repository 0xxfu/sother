"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import inspect
from typing import Type

from slither.detectors import all_detectors as slither_all_detectors
from slither.detectors.abstract_detector import AbstractDetector

from sother.detectors import all_detectors


def get_all_detectors() -> list[Type[AbstractDetector]]:
    detectors_ = [getattr(all_detectors, name) for name in dir(all_detectors)]
    detectors_ += [
        getattr(slither_all_detectors, name)
        for name in dir(slither_all_detectors)
    ]
    return [
        d
        for d in detectors_
        if inspect.isclass(d) and issubclass(d, AbstractDetector)
    ]
