"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest
from abc import ABC
from typing import List

from slither.core.cfg.node import Node

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractTransferInstance,
)

"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from slither.core.expressions import BinaryOperation, CallExpression

"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.analyses.data_dependency.data_dependency import is_dependent
from slither.core.declarations import (
    FunctionContract,
    SolidityVariableComposed,
    Contract,
    Function,
)
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.slithir.operations import Binary, InternalCall, Operation, HighLevelCall
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class Erc721OnReceived(AbstractTransferInstance, ABC):
    @classmethod
    def _has_implement_on_received(cls, contract: Contract) -> bool:
        return any(
            [
                function.solidity_signature
                == "onERC721Received(address,address,uint256,bytes)"
                for function in contract.functions
            ]
        )

    @classmethod
    def _is_transfer_to_this(cls, node: Node) -> bool:
        for ir in node.irs:
            if cls.is_erc721_transfer_instance(ir):
                # `safeTransferFrom(address,address,uint256)`
                # address(this) in second param
                return ",address(this)," in str(ir.expression)
        return False

    @classmethod
    def _is_transfer_from_this(cls, node: Node) -> bool:
        for ir in node.irs:
            if cls.is_erc721_transfer_instance(ir):
                # `safeTransferFrom(address,address,uint256)`
                # address(this) in first param
                return "address(this)," in str(ir.expression)
        return False


class MissingErc721Received(Erc721OnReceived, AbstractDetector):
    ARGUMENT = "missing-erc721-received"
    HELP = "`onERC721Received` not implemented in ERC721 received contract"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki
    WIKI_TITLE = "`onERC721Received` not implemented in ERC721 received contract"

    WIKI_DESCRIPTION = """
The contract does not implement the `onERC721Received` function, 
which is considered a best practice to transfer ERC721 tokens from contracts to contracts. 
The absence of this function could prevent the contract from receiving ERC721 tokens 
from other contracts via `safeTransferFrom/transferFrom`.
"""
    WIKI_EXPLOIT_SCENARIO = """ """

    WIKI_RECOMMENDATION = """
Consider adding an implementation of the `onERC721Received` function in the contract.
"""

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            if self._has_implement_on_received(contract):
                continue
            result_nodes: set[Node] = set()
            for function in contract.functions:
                for node in function.nodes:
                    if self._is_transfer_to_this(node):
                        result_nodes.add(node)
            if len(result_nodes) > 0:
                info: DETECTOR_INFO = [
                    contract,
                    " received NFT via following operations by is missing `onERC721Received` function: \n",
                ]
                for node in result_nodes:
                    info += [f"\t- ", node, "\n"]

                results.append(self.generate_result(info))
        return results


if __name__ == "__main__":
    unittest.main()
