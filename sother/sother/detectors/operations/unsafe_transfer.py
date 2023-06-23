"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from abc import ABC
from typing import List

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.declarations import Function
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.slithir.operations import Operation, HighLevelCall
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class UnSafeTransfer:
    pass


class UnSafeTransferErc20(AbstractDetector, ABC):
    # detector `unchecked-transfer` instead
    pass


class UnsafeTransferErc721(AbstractDetector):
    ARGUMENT = "unsafe-transfer-erc721"

    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.MEDIUM
    WIKI = DetectorSettings.default_wiki

    HELP = (
        "Using `ERC721.transferFrom()` may cause the user's NFT to be frozen in a contract "
        "that does not support ERC721"
    )

    WIKI_TITLE = (
        "Using `ERC721.transferFrom()` may cause the user's NFT to be frozen in a "
        "contract that does not support ERC721"
    )

    WIKI_DESCRIPTION = """
ERC721 NFTs may get locked forever if the recipient is not aware of ERC721 for some reason. 
While `safeTransferFrom()` is used for ERC1155 NFTs (which has the `_doSafeTransferAcceptanceCheck` 
check on recipient and does not have an option to avoid this), `transferFrom()` is used for 
ERC721 NFTs presumably for gas savings and reentrancy concerns over its `safeTransferFrom` 
variant (which has the `_checkOnERC721Received` check on the recipient).
"""
    WIKI_EXPLOIT_SCENARIO = """
if `_to` is a contract address that does not support ERC721, the NFT can be frozen in 
that contract.

As per the documentation of EIP-721:
> A wallet/broker/auction application MUST implement the wallet interface if it will 
accept safe transfers.

Ref: https://eips.ethereum.org/EIPS/eip-721
"""
    WIKI_RECOMMENDATION = """
Evaluate using ERC721 `safeTransferFrom()` to avoid NFTs getting stuck vis-a-vis its 
reentrancy risk and gas costs.
"""

    def _detect(self) -> List[Output]:
        results = []
        for c in self.compilation_unit.contracts:
            for f in c.functions + c.modifiers:
                if f.contract_declarer != c:
                    continue
                erc721_transfers = self.detect_erc721_transfer(f)
                if erc721_transfers:
                    for node in erc721_transfers:
                        info: DETECTOR_INFO = [
                            node,
                            " should be replaced by `safeTransferFrom()`.",
                            "\n",
                        ]

                        res = self.generate_result(info)

                        results.append(res)
        return results

    @classmethod
    def detect_erc721_transfer(cls, function: Function) -> list[Node]:
        result_nodes: list[Node] = list()
        for node in function.nodes:
            for ir in node.irs:
                if cls._is_instance(ir):
                    result_nodes.append(node)
        return result_nodes

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        if (
            isinstance(ir, HighLevelCall)
            and isinstance(ir.function, Function)
            and ir.function.solidity_signature
            in ["transferFrom(address,address,uint256)"]
        ):
            (name, parameters, returnVars) = ir.function.signature
            # returnVars == ["bool"] is erc20
            # erc721 has not return value
            return len(returnVars) == 0

        return False


if __name__ == "__main__":
    unittest.main()
