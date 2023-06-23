"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from abc import ABC, abstractmethod
from typing import List

from slither.core.cfg.node import Node
from slither.core.declarations import Function
from slither.detectors.abstract_detector import AbstractDetector, DETECTOR_INFO
from slither.slithir.operations import Operation
from slither.utils.output import Output


class AbstractDetectHasInstance(AbstractDetector, ABC):
    @classmethod
    @abstractmethod
    def _is_instance(cls, ir: Operation) -> bool:
        pass

    @classmethod
    @abstractmethod
    def _detect_node_info(cls) -> str:
        pass

    def _detect(self) -> List[Output]:
        results = []
        for c in self.compilation_unit.contracts:
            for f in c.functions + c.modifiers:
                if f.contract_declarer != c:
                    continue
                instance_nodes = self.detect_has_instance(f)
                if instance_nodes:
                    for node in instance_nodes:
                        info: DETECTOR_INFO = [
                            node,
                            self._detect_node_info(),
                            "\n",
                        ]
                        res = self.generate_result(info)

                        results.append(res)
        return results

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
