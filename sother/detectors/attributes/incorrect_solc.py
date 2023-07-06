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

    def _check_version(self, version: Tuple[str, str, str, str, str]) -> Optional[str]:
        op = version[0]
        if op and op not in [">", ">=", "^"]:
            return self.LESS_THAN_TXT
        version_number = ".".join(version[2:])
        if version_number in self.BUGGY_VERSIONS:
            return self.BUGGY_VERSION_TXT
        if version_number not in self.ALLOWED_VERSIONS:
            # remove check TOO_RECENT_VERSION_TXT
            return self.OLD_VERSION_TXT
        return None


if __name__ == "__main__":
    unittest.main()
