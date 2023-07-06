"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from slither.detectors.abstract_detector import DetectorClassification
from slither.detectors.statements.boolean_constant_equality import (
    BooleanEquality as SlitherBooleanEquality,
)


class BooleanEquality(SlitherBooleanEquality):
    HELP = "Don't compare booleans to `true` or `false`"

    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = (
        "https://github.com/crytic/slither/wiki/Detector-Documentation#boolean-equality"
    )

    WIKI_TITLE = "Don't compare booleans to `true` or `false`"
    WIKI_DESCRIPTION = """
`true` and `false` are constants and it is more expensive comparing a boolean against them 
than directly checking the returned boolean value
"""


if __name__ == "__main__":
    unittest.main()
