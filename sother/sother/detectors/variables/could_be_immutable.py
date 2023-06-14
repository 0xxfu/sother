"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from slither.detectors.variables.could_be_immutable import (
    CouldBeImmutable as SliCouldBeImmutable,
)


class CouldBeImmutable(SliCouldBeImmutable):
    WIKI_TITLE = "State variables only set in the constructor should be declared immutable"
    WIKI_DESCRIPTION = """
Avoids a Gsset (20000 gas) in the constructor, and replaces the first access in each transaction (Gcoldsload - 2100 gas) and each access thereafter (Gwarmacces - 100 gas) with a PUSH32 (3 gas).

While strings are not value types, and therefore cannot be immutable/constant if not hard-coded outside of the constructor, the same behavior can be achieved by making the current contract abstract with virtual functions for the string accessors, and having a child contract override the functions with the hard-coded implementation-specific values.
    """
    WIKI_RECOMMENDATION = "Add the `immutable` attribute to state variables that never change or are set only in the constructor."


if __name__ == "__main__":
    unittest.main()
