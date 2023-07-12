"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from abc import ABC, abstractmethod
from typing import List, Optional

from loguru import logger
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
                if node in result_nodes:
                    break
                if cls._is_instance(ir):
                    result_nodes.add(node)
        return result_nodes


class AbstractTransferInstance:
    erc20_transfer_signature: list[str] = [
        "transfer(address,uint256)",
        "transferFrom(address,address,uint256)",
        "safeTransfer(address,address,uint256)",
        "safeTransferFrom(address,address,address,uint256)",
    ]

    erc721_transfer_signature: list[str] = [
        "transferFrom(address,address,uint256)",
        "safeTransferFrom(address,address,uint256)",
        "safeTransferFrom(address,address,uint256,bytes)",
    ]

    @classmethod
    def is_erc20_transfer_instance(cls, ir: Operation) -> bool:
        if isinstance(ir, HighLevelCall) and isinstance(ir.function, Function):
            if (
                ir.function.solidity_signature == cls.erc20_transfer_signature[0]
                or ir.function.solidity_signature == cls.erc20_transfer_signature[3]
            ):
                return True
            elif ir.function.solidity_signature in cls.erc20_transfer_signature:
                # if the third param name is `tokenId`, it will be ERC721 token
                # otherwise ERC20
                return "tokenId" not in ir.function.parameters[2].name
        return False

    @classmethod
    def is_erc721_transfer_instance(cls, ir: Operation) -> bool:
        if isinstance(ir, HighLevelCall) and isinstance(ir.function, Function):
            # `safeTransferFrom(address,address,uint256,bytes)`
            # erc20 doesn't has bytes param.
            if ir.function.solidity_signature == cls.erc721_transfer_signature[2]:
                return True
            elif ir.function.solidity_signature in cls.erc721_transfer_signature:
                return "token" in ir.function.parameters[2].name
        return False

    @classmethod
    def get_erc20_transfer_to(cls, ir: HighLevelCall) -> Optional[Variable]:
        transfer_to: Optional[Variable] = None
        if ir.function.solidity_signature == cls.erc20_transfer_signature[0]:
            transfer_to = ir.arguments[0]
        elif ir.function.solidity_signature == cls.erc20_transfer_signature[1]:
            transfer_to = ir.arguments[1]
        elif ir.function.solidity_signature == cls.erc20_transfer_signature[2]:
            transfer_to = ir.arguments[1]
        elif ir.function.solidity_signature == cls.erc20_transfer_signature[3]:
            transfer_to = ir.arguments[2]
        return transfer_to

    @classmethod
    def get_erc20_transfer_amount(cls, ir: HighLevelCall) -> Optional[Variable]:
        transfer_amount: Optional[Variable] = None
        if ir.function.solidity_signature == cls.erc20_transfer_signature[0]:
            transfer_amount = ir.arguments[1]
        elif ir.function.solidity_signature == cls.erc20_transfer_signature[1]:
            transfer_amount = ir.arguments[2]
        elif ir.function.solidity_signature == cls.erc20_transfer_signature[2]:
            transfer_amount = ir.arguments[2]
        elif ir.function.solidity_signature == cls.erc20_transfer_signature[3]:
            transfer_amount = ir.arguments[3]
        return transfer_amount


if __name__ == "__main__":
    unittest.main()
