"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
from typing import List

from slither.core.declarations import StructureContract, CustomErrorContract
from slither.core.expressions import CallExpression, Identifier
from slither.core.solidity_types import UserDefinedType
from slither.core.variables import StateVariable, Variable
from slither.core.variables.local_variable import LocalVariable
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.detectors.variables.uninitialized_state_variables import (
    UninitializedStateVarsDetection,
)
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


# override UnusedStateVars
class UnusedStateVars(AbstractDetector):
    ARGUMENT = "unused-state-variables"
    HELP = "Remove or replace unused state variables"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Remove or replace unused state variables"
    WIKI_DESCRIPTION = """
Saves a storage slot. If the variable is assigned a non-zero value, 
saves Gsset (20000 gas). If it's assigned a zero value, saves Gsreset (2900 gas). 
If the variable remains unassigned, there is no gas savings unless the variable is public, 
in which case the compiler-generated non-payable getter deployment cost is saved. 
If the state variable is overriding an interface's public function, 
mark the variable as constant or immutable so that it does not use a storage slot
"""

    WIKI_RECOMMENDATION = """
Remove or replace the unused state variables
"""

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            result_states = self._detect_unused_state(contract)
            for state in result_states:
                json = self.generate_result([state, " is never used."])
                results.append(json)
        return results

    @classmethod
    def _detect_unused_state(cls, contract) -> list[StateVariable]:
        except_states: list[str] = ["__gap"]
        state_variables = contract.state_variables_declared
        written_variables = UninitializedStateVarsDetection._written_variables(contract)
        read_variables = UninitializedStateVarsDetection._read_variables(contract)
        return [
            state
            for state in state_variables
            if state not in read_variables
            and state not in written_variables
            and state.name not in except_states
        ]


class UnusedNamedReturnVariables(AbstractDetector):
    ARGUMENT = "unused-named-return-variables"
    HELP = "Not using the named return variables anywhere in the function is confusing"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = (
        "Not using the named return variables anywhere in the function is confusing"
    )

    WIKI_DESCRIPTION = """
Consider changing the variable to be an unnamed one, 
since the variable is never assigned, nor is it returned by name. 
If the optimizer is not turned on, leaving the code as it is will also waste gas 
for the stack variable.
"""

    WIKI_RECOMMENDATION = """
Remove the unused named return variables.
"""

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            if contract.is_interface:
                continue
            for function in contract.functions:
                if not function.is_implemented:
                    continue
                result_vars: set[LocalVariable] = set()
                for return_var in function.returns:
                    if return_var.name and return_var not in function.variables_written:
                        result_vars.add(return_var)
                if len(result_vars) > 0:
                    info: DETECTOR_INFO = [
                        "The named return variables in ",
                        function,
                        " are unused.\n",
                    ]
                    for var in result_vars:
                        info += ["\t- ", var, "\n"]
                    results.append(self.generate_result(info))
        return results


class UnusedParameter(AbstractDetector):
    ARGUMENT = "unused-parameter"
    HELP = "Remove unused parameter variables"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Remove unused parameter variables"

    WIKI_DESCRIPTION = """
Unused parameters variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 

"""

    WIKI_RECOMMENDATION = """
Remove the unused parameter variables.
"""

    def _detect(self) -> List[Output]:
        results = []
        exclude_functions = ["onERC1155Received", "onERC721Received"]
        for contract in self.compilation_unit.contracts_derived:
            if contract.is_interface:
                continue
            for function in contract.functions:
                if not function.is_implemented or function.name in exclude_functions:
                    continue
                result_vars: set[LocalVariable] = set()
                for param_var in function.parameters:
                    if param_var not in function.variables_read:
                        result_vars.add(param_var)
                if len(result_vars) > 0:
                    info: DETECTOR_INFO = [
                        "The param variables in ",
                        function,
                        " are unused.\n",
                    ]

                    for var in result_vars:
                        info += [
                            "\t- ",
                            var,
                            f"{f'`.{str(var.type)}`' if not var.name else ''}\n",
                        ]
                    results.append(self.generate_result(info))
        return results


class UnusedLocalVar(AbstractDetector):
    ARGUMENT = "unused-local-var"
    HELP = "Remove unused local variables"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Remove unused local variables"

    WIKI_DESCRIPTION = """
Unused local variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 
"""

    WIKI_RECOMMENDATION = """
Remove the unused local variables.
"""

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            if contract.is_interface:
                continue
            for function in contract.functions:
                if not function.is_implemented:
                    continue
                result_vars: set[LocalVariable] = set()
                for param_var in function.local_variables:
                    if param_var not in function.variables_read:
                        result_vars.add(param_var)
                if len(result_vars) > 0:
                    info: DETECTOR_INFO = [
                        "The local variables in ",
                        function,
                        " are unused.\n",
                    ]
                    for var in result_vars:
                        info += ["\t- ", var, "\n"]
                    results.append(self.generate_result(info))
        return results


# todo detect all contract
class UnusedStruct(AbstractDetector):
    ARGUMENT = "unused-struct"
    HELP = "Remove unused struct declaration"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Remove unused struct declaration"

    WIKI_DESCRIPTION = """
Unused struct declaration are gas consuming. 
And are a bad code practice. 
Removing those structs can save deployment and improve code quality. 
"""

    WIKI_RECOMMENDATION = """
Remove unused struct declaration.
"""

    @classmethod
    def _detect_struct_in_variables(
        cls, structs: list[StructureContract], variables: list[Variable]
    ) -> list[StructureContract]:
        for var in variables:
            var_type = var.type
            if (
                isinstance(var_type, UserDefinedType)
                and isinstance(var_type.type, StructureContract)
                and var_type.type in structs
            ):
                structs.remove(var_type.type)
        return structs

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            if contract.is_library or contract.is_interface:
                continue

            result_structs: list[StructureContract] = contract.structures_declared
            result_structs = self._detect_struct_in_variables(
                result_structs, contract.state_variables
            )
            for function in contract.functions:
                result_structs = self._detect_struct_in_variables(
                    result_structs, function.variables
                )
            if len(result_structs) > 0:
                info: DETECTOR_INFO = [
                    "The structs declaration in ",
                    contract,
                    " are unused.\n",
                ]
                for var in result_structs:
                    info += ["\t- ", var, "\n"]
                results.append(self.generate_result(info))
        return results


class UnusedError(AbstractDetector):
    ARGUMENT = "unused-error"
    HELP = "Remove unused error definition"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Remove unused error definition"

    WIKI_DESCRIPTION = """
Unused  error definition are gas consuming. 
And are a bad code practice. 
Removing those errors save deployment and improve code quality. 
"""

    WIKI_RECOMMENDATION = """
Remove unused error definition.
"""

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            if contract.is_library or contract.is_interface:
                continue
            result_errors: list[CustomErrorContract] = contract.custom_errors_declared
            for function in contract.functions_and_modifiers:
                for node in function.nodes:
                    if (
                        isinstance(node.expression, CallExpression)
                        and isinstance(node.expression.called, Identifier)
                        and node.expression.called.value in result_errors
                    ):
                        result_errors.remove(node.expression.called.value)

            if len(result_errors) > 0:
                info: DETECTOR_INFO = [
                    "The error definition in ",
                    contract,
                    " are unused.\n",
                ]
                for err in result_errors:
                    info += ["\t- `error ", err.solidity_signature, "`\n"]
                results.append(self.generate_result(info))
        return results
