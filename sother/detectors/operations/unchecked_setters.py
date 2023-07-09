"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest
from collections import defaultdict
from typing import List

from slither.analyses.data_dependency.data_dependency import is_tainted
from slither.core.cfg.node import Node
from slither.core.declarations import FunctionContract
from slither.core.solidity_types.elementary_type import Uint, Int
from slither.core.variables import Variable
from slither.core.variables.local_variable import LocalVariable
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class UncheckedSetters(AbstractDetector):
    ARGUMENT = "unchecked-setters"
    HELP = "Setters should check the input value"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Setters should check the input value"
    WIKI_DESCRIPTION = """
Setters should have initial value check to prevent assigning wrong value to the variable. 
Assignment of wrong value can lead to unexpected behavior of the contract.
"""

    WIKI_RECOMMENDATION = """
Add an upper limit check to the setters function.
"""
    WIKI_EXPLOIT_SCENARIO = " "

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for function in contract.functions_entry_points:
                result_nodes: dict[
                    LocalVariable, set[Node]
                ] = self._detect_unchecked_input(function)
                for var in result_nodes:
                    info: DETECTOR_INFO = [
                        var,
                        " lacks an upper limit check on :\n",
                    ]
                    for node in result_nodes[var]:
                        info += ["\t- ", node, "\n"]
                    res = self.generate_result(info)
                    results.append(res)
        return results

    @classmethod
    def _detect_unchecked_input(
        cls, function: FunctionContract
    ) -> dict[LocalVariable, set[Node]]:
        result_nodes: dict[LocalVariable, set[Node]] = defaultdict(set)
        all_int = Uint + Int
        for node in function.nodes:
            sv_int_written = [
                sv for sv in node.state_variables_written if str(sv.type) in all_int
            ]
            if not sv_int_written:
                continue
            for var in node.local_variables_read:
                if str(var.type) in all_int and is_tainted(
                    var, function, ignore_generic_taint=True
                ):
                    if not cls._has_var_validation(var, node, []):
                        result_nodes[var].add(node)

        return result_nodes

    @classmethod
    def _has_var_validation(
        cls, var: LocalVariable, node: Node, explored: List[Node]
    ) -> bool:
        if node in explored:
            return False
        explored.append(node)

        if (node.contains_if() or node.contains_require_or_assert()) and (
            var in node.variables_read
        ):
            return True

        # Check recursively in all the parent nodes
        for father in node.fathers:
            if cls._has_var_validation(var, father, explored):
                return True
        return False


if __name__ == "__main__":
    unittest.main()
