"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from abc import ABC, abstractmethod
from typing import List, Optional

from slither.core.cfg.node import Node
from slither.core.declarations import Function
from slither.core.variables import Variable
from slither.detectors.abstract_detector import AbstractDetector, DETECTOR_INFO
from slither.slithir.operations import Operation, HighLevelCall
from slither.utils.output import Output


class AbstractDetectHasInstance(AbstractDetector, ABC):
    @classmethod
    @abstractmethod
    def _is_instance(cls, ir: Operation) -> bool:
        pass

    @classmethod
    @abstractmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
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
                        info: DETECTOR_INFO = self._detect_node_info(node)
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


class AbstractTransferInstance(AbstractDetectHasInstance, ABC):
    transfer_signature: list[str] = [
        "transfer(address,uint256)",
        "transferFrom(address,address,uint256)",
        "safeTransfer(address,address,uint256)",
        "safeTransferFrom(address,address,address,uint256)",
    ]

    @classmethod
    def is_transfer_instance(cls, ir: Operation) -> bool:
        return (
            isinstance(ir, HighLevelCall)
            and isinstance(ir.function, Function)
            and ir.function.solidity_signature in cls.transfer_signature
        )

    @classmethod
    def get_transfer_to(cls, ir: HighLevelCall) -> Optional[Variable]:
        transfer_to: Optional[Variable] = None
        if ir.function.solidity_signature == cls.transfer_signature[0]:
            transfer_to = ir.arguments[0]
        elif ir.function.solidity_signature == cls.transfer_signature[1]:
            transfer_to = ir.arguments[1]
        elif ir.function.solidity_signature == cls.transfer_signature[2]:
            transfer_to = ir.arguments[1]
        elif ir.function.solidity_signature == cls.transfer_signature[3]:
            transfer_to = ir.arguments[2]
        return transfer_to

    @classmethod
    def get_transfer_amount(cls, ir: HighLevelCall) -> Optional[Variable]:
        transfer_amount: Optional[Variable] = None
        if ir.function.solidity_signature == cls.transfer_signature[0]:
            transfer_amount = ir.arguments[1]
        elif ir.function.solidity_signature == cls.transfer_signature[1]:
            transfer_amount = ir.arguments[2]
        elif ir.function.solidity_signature == cls.transfer_signature[2]:
            transfer_amount = ir.arguments[2]
        elif ir.function.solidity_signature == cls.transfer_signature[3]:
            transfer_amount = ir.arguments[3]
        return transfer_amount


if __name__ == "__main__":
    unittest.main()
