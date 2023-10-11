import typing as T

from slither.core.declarations import FunctionContract, Modifier
from slither.core.variables.local_variable import LocalVariable
from slither.slithir.variables import LocalIRVariable


class NotLocalVariableError(Exception):
    pass


class ParameterChecker:
    @staticmethod
    def is_parameter(
        var: T.Union[LocalIRVariable, LocalVariable],
        function: T.Union[Modifier, FunctionContract],
    ) -> bool:
        if isinstance(var, LocalVariable):
            var: LocalVariable = var.non_ssa_version
        if not isinstance(var, LocalVariable):
            raise NotLocalVariableError(
                f"Variable: {var}, type: {type(var)} is not LocalV(IR)Variable."
            )
        if var in function.parameters:
            return True
        else:
            return False
