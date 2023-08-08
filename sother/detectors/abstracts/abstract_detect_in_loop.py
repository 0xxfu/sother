"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from abc import ABC, abstractmethod
from typing import List, Optional

from slither.core.cfg.node import Node, NodeType
from slither.core.declarations import FunctionContract
from slither.detectors.abstract_detector import AbstractDetector
from slither.slithir.operations import InternalCall, Operation


class AbstractDetectInLoop(AbstractDetector, ABC):
    @classmethod
    @abstractmethod
    def _is_instance(cls, ir: Operation) -> bool:
        pass

    @classmethod
    def detect_loop_in_function(cls, functions: list[FunctionContract]) -> list[Node]:
        ret: List[Node] = []
        for func in functions:
            cls.instance_in_loop(func.entry_point, 0, [], ret)
        return ret

    @classmethod
    def instance_in_loop(
        cls,
        node: Optional[Node],
        in_loop_counter: int,
        visited: List[Node],
        ret: List[Node],
    ) -> None:
        if node is None:
            return

        if node in visited:
            return
        # shared visited
        visited.append(node)

        # check loop start and end
        if node.type == NodeType.STARTLOOP:
            in_loop_counter += 1
        elif node.type == NodeType.ENDLOOP:
            in_loop_counter -= 1

        if in_loop_counter > 0:
            for ir in node.all_slithir_operations():
                # check length in loop
                if cls._is_instance(ir):
                    ret.append(ir.node)
                    break
                if isinstance(ir, (InternalCall)) and ir.function:
                    cls.instance_in_loop(
                        ir.function.entry_point, in_loop_counter, visited, ret
                    )

        for son in node.sons:
            cls.instance_in_loop(son, in_loop_counter, visited, ret)


if __name__ == "__main__":
    unittest.main()
