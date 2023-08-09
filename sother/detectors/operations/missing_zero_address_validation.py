"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-08
"""
import unittest

from slither.detectors.operations.missing_zero_address_validation import (
    MissingZeroAddressValidation as SlitherMissingZeroAddressValidation,
)


# todo except `if (addr != address(0))` statement
class MissingZeroAddressValidation(SlitherMissingZeroAddressValidation):
    WIKI_DESCRIPTION = "Missing zero address validation."


if __name__ == "__main__":
    unittest.main()
