"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from slither.detectors.abstract_detector import DetectorClassification

from slither.slithir.operations import Operation, LowLevelCall

from sother.detectors.operations.unused_return_values import UnusedReturnValues


class UncheckedLowLevel(UnusedReturnValues):
    ARGUMENT = "unchecked-lowlevel"
    HELP = "Unchecked low-level calls"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = "https://github.com/crytic/slither/wiki/Detector-Documentation#unchecked-low-level-calls"

    WIKI_TITLE = "Unchecked low-level calls"
    WIKI_DESCRIPTION = "The return value of a low-level call is not checked."

    # region wiki_exploit_scenario
    WIKI_EXPLOIT_SCENARIO = """
    ```solidity
    contract MyConc{
        function my_func(address payable dst) public payable{
            dst.call.value(msg.value)("");
        }
    }
    ```
    The return value of the low-level call is not checked, so if the call fails, the Ether will be locked in the contract.
    If the low level is used to prevent blocking operations, consider logging failed calls.
        """
    # endregion wiki_exploit_scenario

    WIKI_RECOMMENDATION = (
        "Ensure that the return value of a low-level call is checked or logged."
    )

    def _is_instance(self, ir: Operation) -> bool:  # pylint: disable=no-self-use
        return isinstance(ir, LowLevelCall)


if __name__ == "__main__":
    unittest.main()
