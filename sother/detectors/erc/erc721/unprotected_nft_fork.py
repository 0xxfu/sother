"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.analyses.data_dependency.data_dependency import is_dependent
from slither.core.declarations import FunctionContract, SolidityVariableComposed
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.slithir.operations import Binary
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class UnprotectedNFTFork(AbstractDetector):
    ARGUMENT = "unprotected-nft-fork"
    HELP = "NFT doesn't handle hard forks"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "NFT doesn't handle hard forks"
    WIKI_DESCRIPTION = """
When there are hard forks, users often have to go through 
[many hoops](https://twitter.com/elerium115/status/1558471934924431363) to ensure that 
they control ownership on every fork. Consider adding `require(1 == chain.chainId)`, 
or the chain ID of whichever chain you prefer, to the functions below, 
or at least include the chain ID in the URI, 
so that there is no confusion about which chain is the owner of the NFT.

"""
    WIKI_EXPLOIT_SCENARIO = """ """

    WIKI_RECOMMENDATION = """
Add the following check:
```
if(block.chainid != 1) { 
    revert(); 
}
```
"""

    @classmethod
    def _is_function_protect_fork(cls, function: FunctionContract) -> bool:
        for node in function.nodes:
            for ir in node.irs:
                if isinstance(ir, Binary):
                    for var_read in ir.read:
                        if is_dependent(
                            var_read, SolidityVariableComposed("block.chainid"), node
                        ):
                            return True
        return False

    def _detect(self) -> list[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for function in contract.functions:
                if function.name != "tokenURI":
                    continue
                if not self._is_function_protect_fork(function):
                    res = self.generate_result(
                        [
                            "Protect NFT from copying in forks at the beginning of :\n",
                            function,
                        ]
                    )
                    results.append(res)

        return results


if __name__ == "__main__":
    unittest.main()
