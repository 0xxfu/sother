"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List, Optional

from loguru import logger
from packaging import version
from slither.core.declarations import Pragma
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
)
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings
from sother.utils.pragma_utils import PragmaUtil


class UpgradeToLatest(AbstractDetector):
    ARGUMENT = "upgrade-to-latest"
    HELP = f"Reduce gas usage by moving to Solidity {DetectorSettings.latest_version} or later"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = f"Reduce gas usage by moving to Solidity {DetectorSettings.latest_version} or later"
    WIKI_DESCRIPTION = "See this [link](https://blog.soliditylang.org/2023/02/22/solidity-0.8.19-release-announcement/#preventing-dead-code-in-runtime-bytecode) for the full details"
    WIKI_RECOMMENDATION = f"Upgrade solidity version to the latest version: {DetectorSettings.latest_version}"

    def _detect(self) -> List[Output]:
        results = []
        for pragma in self.compilation_unit.pragma_directives:
            info = self._detect_pragma(pragma)
            if info:
                result = self.generate_result(
                    [
                        "pragma solidity version ",
                        info,
                        f" should upgrade to the latest version: {DetectorSettings.latest_version}",
                    ]
                )
                results.append(result)
        return results

    def _detect_pragma(self, pragma: Pragma) -> Optional[Pragma]:
        if not pragma.is_solidity_version:
            return None
        version1, version2 = PragmaUtil.get_version(pragma.version)
        latest_version = version.parse(DetectorSettings.latest_version)
        if version1 and version2:
            if latest_version < version.parse(
                version1
            ) or latest_version > version.parse(version2):
                return pragma
        if version1 and not version2:
            if latest_version > version.parse(version1):
                return pragma
        return


if __name__ == "__main__":
    unittest.main()
