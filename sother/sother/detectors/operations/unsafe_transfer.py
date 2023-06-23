"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from abc import ABC

from slither.detectors.abstract_detector import (
    AbstractDetector,
)


class UnSafeTransfer:
    pass


class UnSafeTransferErc20(AbstractDetector, ABC):
    # detector `unchecked-transfer` instead
    pass


if __name__ == "__main__":
    unittest.main()
