"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List, Type, Optional

from slither.core.declarations import FunctionContract
from slither.core.expressions import (
    AssignmentOperation,
    BinaryOperation,
    CallExpression,
)
from slither.core.expressions.expression import Expression
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
)
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class InternalFunctionToInline(AbstractDetector):
    ARGUMENT = "internal-function-to-inline"
    HELP = "`internal` functions only called once can be inlined to save gas"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = (
        "`internal` functions only called once can be inlined to save gas"
    )
    WIKI_DESCRIPTION = """
Not inlining costs **20 to 40 gas** because of two extra `JUMP` instructions and additional stack operations needed for function calls.
more detail see [this](https://docs.soliditylang.org/en/v0.8.20/internals/optimizer.html#function-inlining) and [this](https://blog.soliditylang.org/2021/03/02/saving-gas-with-simple-inliner/)
        """

    WIKI_RECOMMENDATION = (
        "Using inlining replace `internal` function which only called once"
    )

    @classmethod
    def _get_called_from_call_operation(
        cls, internal_func_names: list[str], expression: CallExpression
    ) -> Optional[str]:
        if not isinstance(expression, CallExpression):
            return
        if str(expression.called) not in internal_func_names:
            return
        return str(expression.called)

    @classmethod
    def _get_called_from_binary_operation(
        cls, internal_func_names: list[str], expression: BinaryOperation
    ) -> Optional[str]:
        if not isinstance(expression, BinaryOperation):
            return
        call_exp = expression.expression_right

        if not isinstance(call_exp, CallExpression):
            return
        return cls._get_called_from_call_operation(
            internal_func_names, call_exp
        )

    @classmethod
    def _get_called_internal_functions(
        cls,
        internal_func_names: list[str],
        expression: Expression,
    ) -> Optional[str]:
        if not expression:
            return

        if isinstance(expression, CallExpression):
            return cls._get_called_from_call_operation(
                internal_func_names, expression
            )

        if not isinstance(expression, AssignmentOperation):
            return

        exp_right = expression.expression_right
        if isinstance(exp_right, CallExpression):
            return cls._get_called_from_call_operation(
                internal_func_names, exp_right
            )
        if isinstance(exp_right, BinaryOperation):
            return cls._get_called_from_binary_operation(
                internal_func_names, exp_right
            )

    def _detect(self) -> List[Output]:
        results = []
        internal_functions: dict[str, FunctionContract] = dict()
        internal_func_names: list[str] = []
        for contract in self.compilation_unit.contracts_derived:
            for function in contract.functions:
                if function.visibility == "internal":
                    internal_functions[function.name] = function
                    internal_func_names.append(function.name)
        print(f"func names: {internal_func_names} \n\n")

        called_func_names: dict[str, int] = dict()
        for contract in self.compilation_unit.contracts_derived:
            for function in contract.functions:
                for node in function.nodes:
                    func_name = self._get_called_internal_functions(
                        internal_func_names, node.expression
                    )
                    if not func_name:
                        continue
                    if func_name in called_func_names:
                        called_func_names[func_name] += 1
                    else:
                        called_func_names[func_name] = 1

        print(f"called func names: {called_func_names} \n\n")

        for func_name in called_func_names:
            if called_func_names[func_name] > 1:
                continue
            json = self.generate_result(
                [
                    internal_functions[func_name],
                    " could be inlined to save gas",
                ]
            )
            results.append(json)

        return results


if __name__ == "__main__":
    unittest.main()
