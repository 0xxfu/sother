"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-10
"""
import inspect
import unittest
from typing import Type

from slither.detectors.abstract_detector import AbstractDetector


class DetectorUtils:
    @classmethod
    def get_detectors_from_file(cls, dir_path) -> list[Type[AbstractDetector]]:
        detectors = [getattr(dir_path, name) for name in dir(dir_path)]
        return [
            d
            for d in detectors
            if inspect.isclass(d) and issubclass(d, AbstractDetector)
        ]


if __name__ == "__main__":
    unittest.main()
