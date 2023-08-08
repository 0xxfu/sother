"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-08
"""
import unittest
from abc import ABC, abstractmethod
from typing import Optional

from slither.core.cfg.node import Node, NodeType
from slither.core.declarations import SolidityFunction
from slither.slithir.operations import Operation, InternalCall, SolidityCall


class AbstractDetectInIf(ABC):
    @classmethod
    @abstractmethod
    def _is_instance(cls, ir: Operation) -> bool:
        pass

    @classmethod
    def detect_start_with_if_node(cls, node: Node) -> set[Node]:
        result: set[Node] = set()
        cls.instance_in_if_block(node, 0, [], result)
        return result

    @classmethod
    def instance_in_if_block(
        cls,
        node: Optional[Node],
        in_if_counter: int,
        visited: list[Node],
        ret: set[Node],
    ) -> None:
        if node is None:
            return

        if node in visited:
            return
        # shared visited
        visited.append(node)

        # check if start and end
        if node.type == NodeType.IF:
            in_if_counter += 1
        elif node.type == NodeType.ENDIF:
            in_if_counter -= 1

        if in_if_counter > 0:
            for ir in node.all_slithir_operations():
                if cls._is_instance(ir):
                    ret.add(ir.node)
                    break
                if isinstance(ir, (InternalCall)) and ir.function:
                    cls.instance_in_if_block(
                        ir.function.entry_point, in_if_counter, visited, ret
                    )

            for son in node.sons:
                cls.instance_in_if_block(son, in_if_counter, visited, ret)


class DetectRevertInIf(AbstractDetectInIf):
    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        if isinstance(ir, SolidityCall) and ir.function in [
            SolidityFunction("revert()"),
            SolidityFunction("revert(string)"),
            SolidityFunction("revert "),
        ]:
            return True
        return False


if __name__ == "__main__":
    unittest.main()
