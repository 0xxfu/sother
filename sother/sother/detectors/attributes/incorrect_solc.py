"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List, Tuple, Optional

from slither.detectors.attributes.incorrect_solc import (
    IncorrectSolc as SlitherIncorrectSolc,
)
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class IncorrectSolc(SlitherIncorrectSolc):
    ARGUMENT = "solc-version"

    ALLOWED_VERSIONS = [DetectorSettings.latest_version]
    WIKI_RECOMMENDATION = f"""
Deploy with any of the following Solidity versions:
- {DetectorSettings.latest_version}

The recommendations take into account:
- Risks related to recent releases
- Risks of complex code generation changes
- Risks of new language features
- Risks of known bugs

Use a simple pragma version that allows any of these versions.
Consider using the latest version of Solidity for testing."""


if __name__ == "__main__":
    unittest.main()
