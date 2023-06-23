"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
# from sother.detectors.example_detector import ExampleDetector
from sother.detectors.variables.could_be_immutable import CouldBeImmutable
from sother.detectors.variables.bool_state_variables import BoolStateVariables
from sother.detectors.statements.fetch_storage_to_memory import (
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
from sother.detectors.functions.cache_call_function_result import (
    CacheCallFunctionResult,
)
from sother.detectors.source.safe_math_lib import SafeMathLib
from sother.detectors.functions.dead_code import DeadCode
from sother.detectors.events.unindexed_event import UnindexedEvent
from sother.detectors.statements.operator_and_in_require import OperatorAndInRequire
from sother.detectors.functions.memory_in_parameters import MemoryInParameters
from sother.detectors.operations.unchecked_transfer import UncheckedTransfer
from sother.detectors.operations.payable_calls import PayableCalls
from sother.detectors.statements.unchecked_array_length import UncheckedArrayLength
from sother.detectors.statements.deprecated_assert import DeprecatedAssert
from sother.detectors.operations.external_calls_in_loop import ExternalCallsInLoop
from sother.detectors.upgradeable.unprotected_upgradeable_front_run import (
    UnprotectedUpgradeableFrontRun,
)
from sother.detectors.upgradeable.missing_gap_state_variable import (
    MissingGapStateVariable,
)
from sother.detectors.upgradeable.upgradeable_uninitialized import (
    UpgradeableUninitialized,
)
from sother.detectors.permissions.deprecated_ownable import DeprecatedOwnable
from sother.detectors.operations.deprecated_safe_approve import DeprecatedSafeApprove
from sother.detectors.erc.erc721.unsafe_721_transfer import UnsafeTransferErc721
