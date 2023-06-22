"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
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


class DeprecatedSafeApprove(AbstractDetector):
    ARGUMENT = "deprecated-safe-approve"
    HELP = "`safeApprove()` is deprecated"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "`safeApprove()` is deprecated"
    WIKI_DESCRIPTION = """
[Deprecated](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/token/ERC20/utils/SafeERC20.sol#L38-L45) 
in favor of `safeIncreaseAllowance()` and `safeDecreaseAllowance()`. 
If only setting the initial allowance to the value that means infinite, 
`safeIncreaseAllowance()` can be used instead. The function may currently work, 
but if a bug is found in this version of OpenZeppelin, and the version that you're 
forced to upgrade to no longer has this function, you'll encounter unnecessary delays 
in porting and testing replacement contracts.

"""

    WIKI_RECOMMENDATION = """
As suggested by the [OpenZeppelin comment](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/token/ERC20/utils/SafeERC20.sol#L38-L45),
replace `safeApprove()` with `safeIncreaseAllowance()` or `safeDecreaseAllowance()` instead.
"""
    WIKI_EXPLOIT_SCENARIO = " "

    @classmethod
    def _is_deprecated_instance(cls, ir: Operation) -> bool:
        return (
            isinstance(ir, HighLevelCall)
            and isinstance(ir.function, Function)
            and ir.function.solidity_signature
            in ["safeApprove(address,address,uint256)"]
        )

    def _detect(self) -> List[Output]:
        results = []
        result_nodes: set[Node] = set()
        for c in self.compilation_unit.contracts:
            for f in c.functions + c.modifiers:
                if f.contract_declarer != c:
                    continue
                for n in f.nodes:
                    for ir in n.irs:
                        if self._is_deprecated_instance(ir):
                            result_nodes.add(n)

        for node in result_nodes:
            info: DETECTOR_INFO = ["`", node, "` is deprecated."]
            res = self.generate_result(info)
            results.append(res)
        return results


if __name__ == "__main__":
    unittest.main()
