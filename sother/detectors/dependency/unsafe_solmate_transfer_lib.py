"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class UnsafeSolmateTransferLib(AbstractDetector):
    ARGUMENT = "unsafe-solmate-transfer-lib"
    HELP = "Solmate's `SafeTransferLib` doesn't check whether the ERC20 contract exists"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = (
        "Solmate's `SafeTransferLib` doesn't check whether the ERC20 contract exists"
    )

    WIKI_DESCRIPTION = """
Solmate's SafeTransferLib, which is often used to interact with non-compliant/unsafe ERC20 tokens, does not check whether the ERC20 contract exists. The following code will not revert in case the token doesn't exist (yet).

This is stated in the Solmate library: https://github.com/transmissions11/solmate/blob/main/src/utils/SafeTransferLib.sol#L9

Consider using OpenZeppelin's SafeERC20 library instead.
"""

    WIKI_RECOMMENDATION = """
Using OpenZeppelin's `SafeERC20` instead of Solmate's `SafeTransferLib`. 
"""
    WIKI_EXPLOIT_SCENARIO = " "

    def _detect(self) -> list[Output]:
        # todo support UsingFor output
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for using in contract.using_for:
                logger.debug(f"using: {using}")
                for item in contract.using_for[using]:
                    logger.debug(f"item: {item} instance: {type(item)}")
                    if "SafeTransferLib" in str(item):
                        res = self.generate_result(
                            [
                                " Using OpenZeppelin's `SafeERC20` instead of ",
                                f"`{str(item)}`",
                                ".\n",
                            ]
                        )
                        results.append(res)
        return results


if __name__ == "__main__":
    unittest.main()
