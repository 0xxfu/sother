"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from slither.core.cfg.node import Node
from slither.core.declarations import SolidityFunction
from slither.detectors.abstract_detector import DetectorClassification, DETECTOR_INFO
from slither.slithir.operations import Operation, SolidityCall

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings


class MissingMsgInRequire(AbstractDetectHasInstance):
    ARGUMENT = "missing-msg-in-require"
    HELP = "Missing Error Messages in `require/revert` Statements"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Missing Error Messages in `require/revert` Statements"

    WIKI_DESCRIPTION = """
An error message in require statement both helps user and dev to to understand why the execution has failed.
"""

    WIKI_RECOMMENDATION = """
Consider adding error messages in require statement.Ï
"""

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        return isinstance(ir, SolidityCall) and ir.function in [
            SolidityFunction("require(bool)"),
            SolidityFunction("revert()"),
        ]

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            node,
            " is missing message in `require/revert` statement\n",
        ]


if __name__ == "__main__":
    unittest.main()
