"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest
from abc import ABC

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.declarations import (
    Contract,
    FunctionContract,
)
from slither.core.expressions import CallExpression
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.slithir.operations import InternalCall, HighLevelCall
from slither.utils.output import Output

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractTransferInstance,
)
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
                return "From(address(this)," in str(ir.expression)
        return False

    @classmethod
    def _is_checked_received_callback(
        cls, nodes: list[Node], visited: list[Node] = None
    ) -> bool:
        if visited is None:
            visited = list()
        for node in nodes:
            if node in visited:
                continue
            visited.append(node)

            for ir in node.irs:
                if (
                    isinstance(ir, HighLevelCall)
                    and ir.function.solidity_signature
                    == "onERC721Received(address,address,uint256,bytes)"
                ):
                    return True
                elif isinstance(ir, InternalCall) and isinstance(
                    ir.function, FunctionContract
                ):
                    if cls._is_checked_received_callback(ir.function.nodes, visited):
                        return True
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

    def _detect(self) -> list[Output]:
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
                    " received NFT via following operations is missing `onERC721Received` function: \n",
                ]
                for node in result_nodes:
                    info += [f"\t- ", node, "\n"]

                results.append(self.generate_result(info))
        return results


class UncheckedErc721Received(Erc721OnReceived, AbstractDetector):
    ARGUMENT = "unchecked-erc721-received"
    HELP = "`onERC721Received` callback is never called when new tokens are minted or transferred"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki
    WIKI_TITLE = "`onERC721Received` callback is never called when new tokens are minted or transferred"

    WIKI_DESCRIPTION = """
The ERC721 implementation used by the contract does not properly call the
corresponding callback when new tokens are minted or transferred.

The ERC721 standard states that the onERC721Received callback must be called when a
mint or transfer operation occurs.

However, the smart contracts interacting as users of the contracts will not be
notified with the `onERC721Received` callback, as expected according to the ERC721
standard.
"""
    WIKI_EXPLOIT_SCENARIO = """
Alice deploys a contract to interact with the Controller contract to send and receive
ERC721 tokens. Her contract correctly implements the `onERC71Received` callback, but this
is not called when tokens are minted or transferred back to her contract. As a result, the
tokens are trapped.
"""

    WIKI_RECOMMENDATION = """
Short term, ensure that the ERC721 implementations execute the standard callback when
they are required.

Example see OpenZeppelin implementation: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/8b72e20e326078029b92d526ff5a44add2671df1/contracts/token/ERC721/ERC721.sol#L425-L447
"""

    def _detect(self) -> list[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            result_nodes: set[Node] = set()
            for function in contract.functions:
                for node in function.nodes:
                    if self._is_transfer_from_this(
                        node
                    ) and not self._is_checked_received_callback(node.sons):
                        result_nodes.add(node)
            if len(result_nodes) > 0:
                for node in result_nodes:
                    info: DETECTOR_INFO = [
                        node,
                        " unchecked `onERC721Received` callback.\n",
                    ]
                    results.append(self.generate_result(info))
        return results


if __name__ == "__main__":
    unittest.main()
