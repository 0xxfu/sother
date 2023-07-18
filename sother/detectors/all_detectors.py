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
from sother.detectors.operations.assignment_left_operation import (
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
from sother.detectors.operations.use_shifting import DivideByConstant, MulPowerTwo
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
from sother.detectors.erc.erc20.deprecated_safe_approve import DeprecatedSafeApprove
from sother.detectors.erc.erc20.deprecated_approve import DeprecatedApprove
from sother.detectors.erc.erc721.unsafe_721_transfer import UnsafeTransferErc721
from sother.detectors.erc.erc721.unsafe_721_mint import Unsafe721Mint
from sother.detectors.operations.encode_packed import EncodePackedCollision
from sother.detectors.operations.fee_on_transfer import FeeOnTransfer
from sother.detectors.operations.zero_on_transfer import ZeroCheckWithTransfer
from sother.detectors.variables.uninitialized_local_variables import (
    UninitializedLocalVars,
)
from sother.detectors.variables.uninitialized_state_variables import (
    UninitializedStateVarsDetection,
)
from sother.detectors.operations.unused_return_values import UnusedReturnValues
from sother.detectors.operations.zero_address_optimization import (
    ZeroAddressOptimization,
)
from sother.detectors.functions.payable_functions import (
    PayableConstructor,
    PayableFunction,
)
from sother.detectors.operations.pre_plusplus import PrePlusPlus
from sother.detectors.operations.unsigned_int_compare_zero import UnsignedIntCompareZero
from sother.detectors.variables.zero_initialized_state_variable import (
    ZeroInitializedStateVariable,
)
from sother.detectors.variables.constants_optimization import (
    StringConstants,
    CalculateConstants,
    KeccakConstants,
    KeccakConstantInFunctions,
)
from sother.detectors.statements.revert_long_strings import RevertLongStrings
from sother.detectors.variables.address_optimization import AssemblyUpdateAddress
from sother.detectors.functions.external_function import ExternalFunction
from sother.detectors.statements.boolean_constant_equality import BooleanEquality
from sother.detectors.statements.empty_block import EmptyBlock
from sother.detectors.variables.multiple_address_mappings import MultipleAddressMappings
from sother.detectors.operations.unsafe_casting import UnsafeDowncast
from sother.detectors.statements.susceptible_ecrecover import (
    SusceptibleEcrecover,
    UncheckedEcrecover,
)
from sother.detectors.operations.unchecked_setters import UncheckedSetters
from sother.detectors.erc.erc20.revert_on_approve_max import RevertOnApproveMax
from sother.detectors.operations.unsupported_decimals_token import (
    UnsupportedDecimalsToken,
)
from sother.detectors.operations.unsafe_tx_origin import UnsafeTxOrigin
from sother.detectors.operations.unchecked_low_level_return_values import (
    UncheckedLowLevel,
)
from sother.detectors.reentrancy.reentrancy_send_value import ReentrancySendValue
from sother.detectors.pragma.unsafe_floating_pragma import UnsafeFloatingPragma
from sother.detectors.dependency.unsafe_solmate_transfer_lib import (
    UnsafeSolmateTransferLib,
)
from sother.detectors.pragma.unsafe_assembly import UnsafeAssembly
from sother.detectors.events.missing_sender_in_event import MissingSenderInEvent
from sother.detectors.erc.erc721.unprotected_nft_fork import UnprotectedNFTFork
from sother.detectors.upgradeable.unused_upgradeable_counterparts import (
    UnusedUpgradeableCounterparts,
)
from sother.detectors.erc.erc721.unchecked_token_id import UncheckedTokenId
from sother.detectors.erc.erc721.missing_supports_interface import (
    MissingSupportsInterface,
)

from sother.detectors.erc.erc721.non_compliant_erc721 import NonCompliantErc721
from sother.detectors.erc.erc721.missing_erc721_received import (
    MissingErc721Received,
    UncheckedErc721Received,
)
from sother.detectors.source.open_todos import OpenTodos
from sother.detectors.operations.use_selfbalance import (
    UseSelfBalance,
    UseAssemblyBalance,
)
from sother.detectors.statements.use_delete_statement import UseDeleteStatement
from sother.detectors.statements.inefficient_new_bytes import InefficientNewBytes
from sother.detectors.dependency.chainlink import (
    DeprecatedChainLink,
    IgnoredChainlinkReturns,
    UncheckedChainlinkStaleness,
    UncheckedChainlinkRound,
)
from sother.detectors.erc.erc20.revert_on_total_supply import RevertOnTotalSupply
from sother.detectors.statements.incorrect_deadline import IncorrectDeadline
from sother.detectors.reentrancy.reentrancy_transfer import ReentrancyTransfer
