"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from loguru import logger
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.slithir.operations import Operation, HighLevelCall, Transfer, Send
from slither.utils.output import Output

from sother.detectors.abstracts.abstract_detect_in_loop import AbstractDetectInLoop
from sother.detectors.detector_settings import DetectorSettings


# todo only detect: state change and balance change 
class ExternalCallsInLoop(AbstractDetectInLoop):
    ARGUMENT = "external-calls-in-loop"
    HELP = "External calls in an un-bounded `for-`loop may result in a DOS"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "External calls in an un-bounded `for-loop` may result in a DOS"
    WIKI_DESCRIPTION = """
The use of external calls in nested loops and subsequent loops, which iterate over lists that
could have been provided by callers, may result in an out-of-gas failure during execution.
"""
    WIKI_EXPLOIT_SCENARIO = """ """

    WIKI_RECOMMENDATION = """
It is recommended to set the max length to which a for loop can iterate.
If possible, use [pull over push strategy for external calls](https://ethereum-contract-security-techniques-and-tips.readthedocs.io/en/latest/recommendations/#favor-pull-over-push-for-external-calls).
"""

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts:
            result_nodes = self.detect_loop_in_function(contract.functions)
            for node in result_nodes:
                logger.debug(f"external calls in loop: {str(node)}")
                res = self.generate_result(
                    [node, " external calls in loop may result in DOS.\n"]
                )
                results.append(res)
        return results

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        return isinstance(ir, (HighLevelCall, Transfer, Send))


if __name__ == "__main__":
    unittest.main()
