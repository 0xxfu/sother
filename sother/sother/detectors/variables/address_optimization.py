"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest
from typing import List

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.declarations import FunctionContract
from slither.core.expressions import BinaryOperation, AssignmentOperation, Identifier
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings
from sother.utils.gas_utils import GasUtils


class AssemblyUpdateAddress(AbstractDetector):
    ARGUMENT = "assembly-update-address"
    HELP = "Use `assembly` to write address storage values"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Use `assembly` to write address storage values"
    WIKI_DESCRIPTION = """
Where it does not affect readability, 
using assembly for simple setters allows to save gas not only on deployment, 
but also on function calls.
"""

    WIKI_RECOMMENDATION = """
Using `assembly` update address to save gas.

For example:
```
contract Contract1 {
    address owner;

    function assemblyUpdateOwner(address newOwner) public {
        assembly {
            sstore(owner.slot, newOwner)
        }
    }
}
```
"""

    @classmethod
    def _is_update_address_instance(cls, node: Node) -> bool:
        # logger.debug(f"exp: {node.expression} type: {type(node.expression)}")
        node_exp = node.expression
        if (
            isinstance(node_exp, AssignmentOperation)
            and isinstance(node_exp.expression_left, Identifier)
            and isinstance(node_exp.expression_right, Identifier)
            and str(node_exp.expression_left.value.type) == "address"
            and str(node_exp.expression_right.value.type) == "address"
        ):
            return True
        return False

    @classmethod
    def _detect_update_address(cls, function: FunctionContract) -> set[Node]:
        result_nodes: set[Node] = set()
        for node in function.nodes:
            if cls._is_update_address_instance(node):
                result_nodes.add(node)
        return result_nodes

    def _detect(self) -> List[Output]:
        results = []
        for function in GasUtils.get_available_functions(self.compilation_unit):
            result_nodes: set[Node] = self._detect_update_address(function)
            for node in result_nodes:
                json = self.generate_result(
                    [
                        node,
                        " should use `assembly` update address to save gas.\n",
                    ]
                )
                results.append(json)
        return results


if __name__ == "__main__":
    unittest.main()
