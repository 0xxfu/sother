"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from abc import ABC, abstractmethod

from slither.core.cfg.node import Node
from slither.core.declarations import Function
from slither.detectors.abstract_detector import AbstractDetector
from slither.slithir.operations import Operation


class AbstractDetectHasInstance(AbstractDetector, ABC):
    @classmethod
    @abstractmethod
    def _is_instance(cls, ir: Operation) -> bool:
        pass

    @classmethod
    def detect_has_instance(cls, function: Function) -> set[Node]:
        result_nodes: set[Node] = set()
        for node in function.nodes:
            for ir in node.irs:
                if cls._is_instance(ir):
                    result_nodes.add(node)
        return result_nodes


if __name__ == "__main__":
    unittest.main()
