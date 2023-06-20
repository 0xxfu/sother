"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


# todo impl detect
class OpcodePush0(AbstractDetector):
    ARGUMENT = "opcode-push0"
    HELP = f"Solidity version 0.8.20 may not work on other chains due to `PUSH0`"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = f"Solidity version 0.8.20 may not work on other chains due to `PUSH0`"
    WIKI_DESCRIPTION = """
The compiler for Solidity 0.8.20 switches the default target EVM version to [Shanghai](https://blog.soliditylang.org/2023/05/10/solidity-0.8.20-release-announcement/#important-note), which includes the new `PUSH0` op code. This op code may not yet be implemented on all L2s, so deployment on these chains will fail.
"""
    WIKI_RECOMMENDATION = f"""
Using an earlier [EVM](https://docs.soliditylang.org/en/v0.8.20/using-the-compiler.html?ref=zaryabs.com#setting-the-evm-version-to-target) [version](https://book.getfoundry.sh/reference/config/solidity-compiler#evm_version)

"""

    def _detect(self) -> List[Output]:
        results = []
        return results


if __name__ == "__main__":
    unittest.main()
