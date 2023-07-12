"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

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
)
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.slithir.operations import Binary, InternalCall, Return
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class NonCompliantErc721(AbstractDetector):
    ARGUMENT = "non-compliant-erc721"
    HELP = "NFT token do not comply with `ERC721`, breaking composability"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki
    WIKI_TITLE = "NFT token do not comply with `ERC721`, breaking composability"

    WIKI_DESCRIPTION = """
The issue is not comply with ERC721 itself. From [EIP721](https://eips.ethereum.org/EIPS/eip-721):
"Every ERC-721 compliant contract must implement the ERC721 and ERC165 interfaces (subject to “caveats” below):"

interface IDs are calculating by XORing together all the function signatures in the 
interface. Therefore, returning true for IERC721Enumerable and IERC721Metadata will 
not implicitly include IERC721.
"""
    WIKI_EXPLOIT_SCENARIO = """ """

    WIKI_RECOMMENDATION = """
Change supportedInterface function:

```
function supportsInterface(bytes4 interfaceId)
    external
    view
    virtual
    override(IERC165)
    returns (bool)
{
    return
    interfaceId == type(IERC721).interfaceId || 
    interfaceId == type(IERC721Enumerable).interfaceId ||
    interfaceId == type(IERC721Metadata).interfaceId ;
}
```
"""

    supports_interface_inherit_name = ["ERC165", "ERC721"]

    @classmethod
    def _detect_derived_165_in_supports(
        cls, contract: Contract
    ) -> (FunctionContract, set[Contract]):
        result_inherits: set[Contract] = set()
        result_function: FunctionContract = None

        for inherit in contract.inheritance:
            if any(
                ["IERC165" == sub_inherit.name for sub_inherit in inherit.inheritance]
            ):
                result_inherits.add(inherit)
        for function in contract.functions:
            if function.signature_str == "supportsInterface(bytes4) returns(bool)":
                result_function = function
                for node in function.nodes:
                    for ir in node.irs:
                        if isinstance(ir, Return):
                            for inherit in list(result_inherits):
                                inherit_name = (
                                    inherit.name
                                    if inherit.name.startswith("I")
                                    else f"I{inherit.name}"
                                )
                                if f"type()({inherit_name}).interfaceId" in str(
                                    ir.expression
                                ):
                                    result_inherits.remove(inherit)
        return result_function, result_inherits

    def _detect(self) -> list[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            result_function, result_inherits = self._detect_derived_165_in_supports(
                contract
            )
            if len(result_inherits) > 0 and result_function:
                info: DETECTOR_INFO = [
                    result_function,
                    f" of `{contract.name}` is missing support:\n",
                ]
                for inherit in result_inherits:
                    info += [f"\t- ", inherit, "\n"]

                results.append(self.generate_result(info))
        return results


if __name__ == "__main__":
    unittest.main()
