"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from slither.analyses.data_dependency.data_dependency import is_dependent
from slither.core.cfg.node import Node
from slither.core.declarations import SolidityVariableComposed
from slither.detectors.abstract_detector import DetectorClassification, DETECTOR_INFO
from slither.slithir.operations import Operation, EventCall

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings
from sother.utils.function_utils import FunctionUtils


class MissingSenderInEvent(AbstractDetectHasInstance):
    ARGUMENT = "missing-sender-in-event"
    HELP = "Events are missing sender information"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Events are missing sender information"

    WIKI_DESCRIPTION = """
When an action is triggered based on a user's action, not being able to filter based on 
who triggered the action makes event processing a lot more cumbersome. 
Including the `msg.sender` the events of these types of action will make events much more 
useful to end users.

"""

    WIKI_RECOMMENDATION = """
Adding `msg.sender` to event.
"""
    WIKI_EXPLOIT_SCENARIO = " "

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        if ir.node.function.is_constructor or ir.node.function.is_constructor_variables:
            return False
        if not FunctionUtils.is_entry_point_function(ir.node.function):
            return False
        if isinstance(ir, EventCall):
            for var_read in ir.read:
                if is_dependent(
                    var_read, SolidityVariableComposed("msg.sender"), ir.node
                ):
                    return False
                elif any(
                    ["only" in modifier.name for modifier in ir.node.function.modifiers]
                ):
                    return False
            return True
        return False

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            node,
            " should add `msg.sender` to event.",
            "\n",
        ]


if __name__ == "__main__":
    unittest.main()
