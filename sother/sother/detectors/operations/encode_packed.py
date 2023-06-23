"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from slither.detectors.abstract_detector import DetectorClassification
from slither.detectors.operations.encode_packed import (
    EncodePackedCollision as SlitherEncodePackedCollision,
)


class EncodePackedCollision(SlitherEncodePackedCollision):
    IMPACT = DetectorClassification.LOW
    WIKI_TITLE = (
        "`abi.encodePacked()` should not be used with dynamic types when passing "
        "the result to a hash function such as `keccak256()`"
    )
    WIKI_DESCRIPTION = """
Use `abi.encode()` instead which will pad items to 32 bytes, which will 
[prevent hash collisions](https://docs.soliditylang.org/en/v0.8.13/abi-spec.html#non-standard-packed-mode) 
(e.g. `abi.encodePacked(0x123,0x456)` => `0x123456` => `abi.encodePacked(0x1,0x23456)`, 
but `abi.encode(0x123,0x456)` => `0x0...1230...456`). "Unless there is a compelling reason, 
`abi.encode` should be preferred". If there is only one argument to `abi.encodePacked()` 
it can often be cast to `bytes()` or `bytes32()` [instead](https://ethereum.stackexchange.com/questions/30912/how-to-compare-strings-in-solidity#answer-82739).

There is also discussion of [removing abi.encodePacked from future versions of Solidity](https://github.com/ethereum/solidity/issues/11593),
so using `abi.encode` now will ensure compatibility in the future.
"""
    WIKI_RECOMMENDATION = """Do not use more than one dynamic type in `abi.encodePacked()`
    (see the [Solidity documentation](https://docs.soliditylang.org/en/latest/abi-spec.html#non-standard-packed-mode)). 
    Use `abi.encode()`, preferably."""


if __name__ == "__main__":
    unittest.main()
