"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List, Optional

from packaging import version
from slither.core.declarations import Pragma
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


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
        pragma_version = self._get_version(pragma)

        if version.parse(DetectorSettings.latest_version) <= version.parse(
            pragma_version
        ):
            return None
        return pragma

    def _get_version(self, pragma: Pragma) -> str:
        ops = [">", "=", "^"]

        def _remove_op(p_version):
            if p_version[0] in ops:
                p_version = p_version[1:]
                p_version = _remove_op(p_version)
            return p_version

        return _remove_op(pragma.version)


if __name__ == "__main__":
    unittest.main()
