"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.declarations import FunctionContract, Function
from slither.core.variables import Variable
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.slithir.operations import (
    HighLevelCall,
    LowLevelCall,
    LibraryCall,
    InternalCall,
)
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings
from sother.utils.gas_utils import GasUtils


class CacheCallFunctionResult(AbstractDetector):
    ARGUMENT = "cache-call-function-result"
    HELP = "The result of function calls should be cached rather than re-calling the function"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "The result of function calls should be cached rather than re-calling the function"
    WIKI_DESCRIPTION = """
The instances below point to the second+ call of the function within a single function
"""

    WIKI_RECOMMENDATION = """
Using local variable to cache function called result if the same function called more than once.
"""

    def _detect(self) -> List[Output]:
        """
        1. get called function which doesn't contain param
        2. count the same function call
        3. return the dict(Function,set[Node])
        """
        results = []
        for function in GasUtils.get_available_functions(self.compilation_unit):
            result_nodes = self._detect_function_call(function)
            for function_called_name in result_nodes:
                logger.debug(f"function called >=2: {function_called_name}")
                result = [
                    f"`{function_called_name}`",
                    " called result should be cached with local variable in ",
                    function,
                    ", It is called more than once:\n",
                ]
                for node in result_nodes[function_called_name]:
                    result += ["\t- ", node, "\n"]
                res = self.generate_result(result)
                results.append(res)
        return results

    @classmethod
    def _detect_function_call(cls, function: FunctionContract) -> dict[str, set[Node]]:
        result_nodes: dict[str, set[Node]] = dict()
        function_called_counts: dict[str, set[Node]] = dict()
        for node in function.nodes:
            for ir in node.irs:
                if (
                    isinstance(ir, (HighLevelCall, InternalCall))
                    and isinstance(ir.function, Function)
                    and len(ir.arguments) <= 0
                ):
                    function_called_name = ir.function.canonical_name

                    if function_called_name not in function_called_counts:
                        function_called_counts[function_called_name] = set()
                    function_called_counts[function_called_name].add(node)

                    if len(function_called_counts[function_called_name]) > 1:
                        result_nodes[function_called_name] = function_called_counts[
                            function_called_name
                        ]

        return result_nodes


if __name__ == "__main__":
    unittest.main()
