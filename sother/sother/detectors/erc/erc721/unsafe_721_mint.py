"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from loguru import logger
from slither.core.declarations import Function
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.slithir.operations import Operation, HighLevelCall, InternalCall
from slither.utils.output import Output

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings


class Unsafe721Mint(AbstractDetectHasInstance):
    ARGUMENT = "unsafe-721-mint"

    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.MEDIUM
    WIKI = DetectorSettings.default_wiki

    HELP = "Use `_safeMint` instead of `_mint` for ERC721"

    WIKI_TITLE = "Use `_safeMint` instead of `_mint` for ERC721"

    WIKI_DESCRIPTION = """
`_mint()` is [discouraged](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/d4d8d2ed9798cc3383912a23b5e8d5cb602f7d4b/contracts/token/ERC721/ERC721.sol#L271) in favor of `_safeMint()` 
which ensures that the recipient is either an EOA or implements `IERC721Receiver`. 
Both [OpenZeppelin](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/d4d8d2ed9798cc3383912a23b5e8d5cb602f7d4b/contracts/token/ERC721/ERC721.sol#L238-L250) and [solmate](https://github.com/Rari-Capital/solmate/blob/4eaf6b68202e36f67cab379768ac6be304c8ebde/src/tokens/ERC721.sol#L180) 
have versions of this function
"""
    WIKI_EXPLOIT_SCENARIO = """
if `to` is a contract address that does not support ERC721, the NFT can be frozen in the contract.

As per the documentation of EIP-721:

> A wallet/broker/auction application MUST implement the wallet interface if it will accept safe transfers.

Ref: https://eips.ethereum.org/EIPS/eip-721

As per the documentation of ERC721.sol by Openzeppelin

Ref: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol#L260-L272

```
    /**
     * @dev Mints `tokenId` and transfers it to `to`.
     *
     * WARNING: Usage of this method is discouraged, use {_safeMint} whenever possible
     *
     * Requirements:
     *
     * - `tokenId` must not exist.
     * - `to` cannot be the zero address.
     *
     * Emits a {Transfer} event.
     */
    function _mint(address to, uint256 tokenId) internal virtual {
```

"""
    WIKI_RECOMMENDATION = """
Use `_safeMint` instead of `_mint` to check received address support for ERC721 implementation.

Ref: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol#L249-L258

"""

    @classmethod
    def _detect_node_info(cls) -> str:
        return " should be replaced by `_safeMint()`."

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        return (
            isinstance(ir, InternalCall)
            and isinstance(ir.function, Function)
            and ir.node.function.name != "_safeMint"
            and ir.function.solidity_signature in ["_mint(address,uint256)"]
        )


if __name__ == "__main__":
    unittest.main()
