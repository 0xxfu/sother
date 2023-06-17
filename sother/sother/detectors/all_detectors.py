"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
# from sother.detectors.example_detector import ExampleDetector
from sother.detectors.variables.could_be_immutable import CouldBeImmutable
from sother.detectors.variables.bool_state_variables import BoolStateVariables
from sother.detectors.variables.fetch_storage_to_memory import (
    FetchStorageToMemory,
)
from sother.detectors.pragma.upgrade_to_latest import UpgradeToLatest
from sother.detectors.attributes.incorrect_solc import IncorrectSolc
from sother.detectors.statements.assignment_left_operation import (
    AssignmentLeftOperation,
)
from sother.detectors.functions.internal_function_to_inline import (
    InternalFunctionToInline,
)
from sother.detectors.statements.array_length_in_loop import ArrayLengthInLoop
from sother.detectors.statements.unchecked_in_loop import UncheckedInLoop
from sother.detectors.statements.used_custom_error import UsedCustomError
from sother.detectors.variables.smaller_uint_int import SmallerUintInt
from sother.detectors.variables.public_to_private_constant import (
    PublicToPrivateConstant,
)
from sother.detectors.variables.reread_state_variables import RereadStateVariables
from sother.detectors.variables.unused_state_variables import UnusedStateVariables
from sother.detectors.operations.divide_by_constant import DivideByConstant
from sother.detectors.events.superfluous_fields_event import SuperfluousFieldsEvent
