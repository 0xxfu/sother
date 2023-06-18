"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List, Union

from loguru import logger
from packaging import version
from slither.core.declarations import Contract, Function
from slither.core.solidity_types import Type
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings
from sother.utils.pragma_utils import PragmaUtil


class SafeMathLib(AbstractDetector):
    ARGUMENT = "safe-math-lib"
    HELP = "Don't use `SafeMath` if use solidity version `>=0.8.0`"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Don't use `SafeMath` if use solidity version `>=0.8.0`"
    WIKI_DESCRIPTION = """
Version `>=0.8.0` introduces internal overflow checks, using `SafeMath` function calls will be more expensive than just built in arithmetic, so using SafeMath is redundant and adds overhead.

More detail see [Solidity 0.8.0 Release Announcement][https://blog.soliditylang.org/2020/12/16/solidity-v0.8.0-release-announcement/#:~:text=the%20full%20list!-,Checked%20Arithmetic,-The%20%E2%80%9CChecked%20Arithmetic] and [OpenZeppelin discussion](https://github.com/OpenZeppelin/openzeppelin-contracts/issues/2465)
"""

    WIKI_RECOMMENDATION = """
Remove `SafeMath` lib.
"""

    def _detect(self) -> List[Output]:
        results = []
        pragmas = self.compilation_unit.pragma_directives
        safe_math_version = version.parse("0.8.0")
        greater_than_safe_math = False
        for pragma in pragmas:
            version1, version2 = PragmaUtil.get_version(pragma.version)
            if version1 and version.parse(version1) > safe_math_version:
                logger.debug(
                    f"safe math version: {safe_math_version} "
                    f"current version: {version1}"
                )
                greater_than_safe_math = True
        if not greater_than_safe_math:
            return results

        contract_using_for: dict[Contract, Union[Type, Function]] = dict()
        for contract in self.compilation_unit.contracts_derived:
            using_for = contract.using_for_complete
            for key in using_for:
                for item in using_for[key]:
                    if str(item) == "SafeMath":
                        contract_using_for[contract] = item

        for contract in contract_using_for:
            logger.debug(f"using:  {contract_using_for[contract]} in {contract}")
            result = self.generate_result(
                [
                    f"`SafeMath` used in ",
                    contract,
                    f" should be removed",
                ]
            )
            results.append(result)

        return results


if __name__ == "__main__":
    unittest.main()
