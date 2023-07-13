"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.solidity_types import ElementaryType
from slither.detectors.abstract_detector import DetectorClassification, DETECTOR_INFO
from slither.slithir.operations import Operation, Assignment, NewElementaryType
from slither.slithir.variables import Constant

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings


class InefficientNewBytes(AbstractDetectHasInstance):
    ARGUMENT = "inefficient-new-bytes"
    HELP = 'Expression `""` is cheaper than `new bytes(0)`'
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = 'Expression `""` is cheaper than `new bytes(0)`'

    WIKI_DESCRIPTION = """

"""

    WIKI_RECOMMENDATION = """
Using empty string `""` instead of `new bytes(0)`.
"""

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        if isinstance(ir, NewElementaryType) and str(ir.expression) == "new bytes(0)":
            return True
        return False

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            'Should use `""` instead of `new bytes(0)` on ',
            node,
            "\n",
        ]


if __name__ == "__main__":
    unittest.main()
