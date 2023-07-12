"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.analyses.data_dependency.data_dependency import is_dependent
from slither.core.declarations import FunctionContract, SolidityVariableComposed
from slither.core.expressions import BinaryOperation
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.slithir.operations import Binary, InternalCall
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class UncheckedTokenId(AbstractDetector):
    ARGUMENT = "unchecked-token-id"
    HELP = "`tokenURI()` does not follow EIP-721"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "`tokenURI()` does not follow EIP-721"

    WIKI_DESCRIPTION = """
The [EIP](https://eips.ethereum.org/EIPS/eip-721) states that `tokenURI()` 
"Throws if `_tokenId` is not a valid NFT", which the code below does not do. 
f the NFT has not yet been minted, `tokenURI()` should revert.

"""
    WIKI_EXPLOIT_SCENARIO = """ """

    WIKI_RECOMMENDATION = """
Check if `tokenId` has minted at the beginning of `tokenURI` function.

For example:
```
    function tokenURI(uint256 tokenId) public view virtual returns (string memory) {
        if (_owners[tokenId] == address(0)) {
            revert("err");
        }

        string memory baseURI = _baseURI();
        return bytes(baseURI).length > 0 ? string.concat(baseURI, tokenId.toString()) : "";
    }
```
"""

    @classmethod
    def _is_function_check_token_id(
        cls, function: FunctionContract, visited=None
    ) -> bool:
        if visited is None:
            visited = list()
        if function in visited:
            return False
        for node in function.nodes:
            if isinstance(node.expression, BinaryOperation):
                for var_read in node.local_variables_read:
                    for param in function.parameters:
                        if is_dependent(var_read, param, node):
                            return True
            else:
                for ir in node.irs:
                    if isinstance(ir, InternalCall) and isinstance(
                        ir.function, FunctionContract
                    ):
                        if cls._is_function_check_token_id(ir.function, visited):
                            return True

        return False

    def _detect(self) -> list[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for function in contract.functions:
                if function.name != "tokenURI":
                    continue
                if not self._is_function_check_token_id(function):
                    res = self.generate_result(
                        [
                            "Check if `tokenId` has minted at the beginning of :\n",
                            function,
                        ]
                    )
                    results.append(res)

        return results


if __name__ == "__main__":
    unittest.main()
