"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from slither.detectors.abstract_detector import DetectorClassification
from slither.detectors.operations.unchecked_transfer import (
    UncheckedTransfer as SlitherUncheckedTransfer,
)


class UncheckedTransfer(SlitherUncheckedTransfer):
    ARGUMENT = "unchecked-transfer"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.MEDIUM
    HELP = "Return values of `transfer()/transferFrom()` not checked"
    WIKI_TITLE = "Return values of `transfer()/transferFrom()` not checked"
    WIKI_DESCRIPTION = """
Not all `IERC20` implementations `revert()` when there's a failure in `transfer()`/`transferFrom()`. The function signature has a `boolean` return value and they indicate errors that way instead. By not checking the return value, operations that should have marked as failed, may potentially go through without actually making a payment.
"""


# todo impl
class UnsafeTransfer:
    pass


if __name__ == "__main__":
    unittest.main()
