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
from sother.detectors.statements.loop_array_length import LoopArrayLength
