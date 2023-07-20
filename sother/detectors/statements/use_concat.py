"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.declarations import SolidityFunction
from slither.core.solidity_types import ElementaryType
from slither.core.solidity_types.elementary_type import Byte
from slither.core.variables import Variable
from slither.detectors.abstract_detector import DetectorClassification, DETECTOR_INFO
from slither.slithir.operations import Operation, SolidityCall

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings


class UseConcatOnString(AbstractDetectHasInstance):
    ARGUMENT = "use-concat-on-string"
    HELP = "Use `string.concat()` on string instead of `abi.encodePacked()` to save gas"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = (
        "Use `string.concat()` on string instead of `abi.encodePacked()` to save gas"
    )

    WIKI_DESCRIPTION = """
Starting with version 0.8.12, 
Solidity has the `string.concat()` function, 
which allows one to concatenate a list of strings, without extra padding. 
Using this function rather than `abi.encodePacked()` makes the intended operation more clear, 
leading to less reviewer confusion and saving more gas.
"""

    WIKI_RECOMMENDATION = """
Use `string.concat()` on string instead of `abi.encodePacked()`
"""

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        return (
            isinstance(ir, SolidityCall)
            and ir.function == SolidityFunction("abi.encodePacked()")
            and all(
                [
                    isinstance(var, Variable) and var.type == ElementaryType("string")
                    for var in ir.read
                ]
            )
        )

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            "should use `string.concat()` on string instead of ",
            node,
            "\n",
        ]


class UseConcatOnBytes(AbstractDetectHasInstance):
    ARGUMENT = "use-concat-on-bytes"
    HELP = "Use `bytes.concat()` on mixing bytes and strings instead of `abi.encodePacked()` to save gas"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Use `bytes.concat()` on mixing bytes and strings instead of `abi.encodePacked()` to save gas"

    WIKI_DESCRIPTION = """
Starting with version 0.8.4, 
Solidity has the `bytes.concat()` function, 
which allows one to concatenate a list of bytes/strings, without extra padding. 
Using this function rather than `abi.encodePacked()` makes the intended operation more clear, 
leading to less reviewer confusion and saving more gas.
"""

    WIKI_RECOMMENDATION = """
Use `bytes.concat()` on mixing bytes and strings instead of `abi.encodePacked()`
"""

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        return (
            isinstance(ir, SolidityCall)
            and ir.function == SolidityFunction("abi.encodePacked()")
            and all(
                [
                    any(
                        [
                            isinstance(var, Variable)
                            and var.type == ElementaryType("string")
                            for var in ir.read
                        ]
                    ),
                    any(
                        [
                            isinstance(var, Variable) and str(var.type) in Byte
                            for var in ir.read
                        ]
                    ),
                ]
            )
        )

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            "should use `bytes.concat()` on mixing bytes and strings instead of  ",
            node,
            "\n",
        ]


if __name__ == "__main__":
    unittest.main()
