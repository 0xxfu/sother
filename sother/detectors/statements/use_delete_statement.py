"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from slither.core.cfg.node import Node, NodeType
from slither.core.solidity_types import ElementaryType
from slither.detectors.abstract_detector import DetectorClassification, DETECTOR_INFO
from slither.slithir.operations import Operation, Assignment
from slither.slithir.variables import Constant

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings


class UseDeleteStatement(AbstractDetectHasInstance):
    ARGUMENT = "use-delete-statement"
    HELP = "Use `delete` to Clear Variables"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Use `delete` to Clear Variables"

    WIKI_DESCRIPTION = """
delete a assigns the initial value for the type to a. i.e. 
for integers it is equivalent to a = 0, but it can also be used on arrays, 
where it assigns a dynamic array of length zero or a static array of the same 
length with all elements reset. For structs, it assigns a struct with all members reset. 
Similarly, it can also be used to set an address to zero address. 
It has no effect on whole mappings though (as the keys of mappings may be arbitrary 
and are generally unknown). However, individual keys and what they map to can be deleted: 
If a is a mapping, then delete a[x] will delete the value stored at x.

The delete key better conveys the intention and is also more idiomatic. 
Consider replacing assignments of zero with delete statements.
"""

    WIKI_RECOMMENDATION = """
Replacing assignments of zero with delete statements.

"""

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        if isinstance(ir, Assignment) and isinstance(ir.rvalue.type, ElementaryType):
            rvalue = ir.rvalue
            # except declaration in loop `for (uint i = 0; i < 10;)`
            for son in ir.node.sons:
                if son.type == NodeType.STARTLOOP:
                    return False
            if isinstance(rvalue, Constant) and rvalue.value in [0, False]:
                return True
            elif str(rvalue.type) == "address" and "address(0)" in str(ir.expression):
                return True
        return False

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            "Should use `delete` statement instead of ",
            node,
            "\n",
        ]


if __name__ == "__main__":
    unittest.main()
