"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from slither.core.declarations import FunctionContract
from slither.core.expressions import AssignmentOperation
from slither.core.variables import StateVariable
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
)
from slither.utils.output import Output
from slither.visitors.expression.export_values import ExportValues

from sother.detectors.detector_settings import DetectorSettings


# arithmetic operator =
# assignment operator += -=
class AssignmentLeftOperation(AbstractDetector):
    ARGUMENT = "assignment-left-operation"
    HELP = "`<x> += <y>` costs more gas than `<x> = <x> + <y>` for state variables"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "`<x> += <y>` costs more gas than `<x> = <x> + <y>` for state variables"
    WIKI_DESCRIPTION = """Using the addition operator instead of plus-equals saves **[113 gas](https://gist.github.com/0xxfu/86ae4bdd07d7db169cea110dba5a5af4)**"""

    WIKI_RECOMMENDATION = "Using arithmetic operator `=` replace assignment operator `+=` or `-=` "

    LEFT_OPERATIONS = ["+=", "-="]

    def _detect(self) -> List[Output]:
        self.results = []
        for contract in self.compilation_unit.contracts_derived:
            for function in contract.functions:
                self._detect_function_assignment(function)
        return self.results

    def _detect_function_assignment(self, function: FunctionContract):
        state_variables: list[StateVariable] = function.state_variables_written
        state_names = [state.name for state in state_variables]

        for node in function.nodes:
            node_expression = node.expression
            if not isinstance(node_expression, AssignmentOperation):
                continue
            if str(node_expression.expression_left) not in state_names:
                continue
            if str(node_expression.type) not in self.LEFT_OPERATIONS:
                continue

            json = self.generate_result(
                [
                    "should use arithmetic operator `=` replace ",
                    f"`{str(node_expression.type)}` in ",
                    node,
                ]
            )
            self.results.append(json)


if __name__ == "__main__":
    unittest.main()
