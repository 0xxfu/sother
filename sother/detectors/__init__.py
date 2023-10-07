"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import inspect
import unittest
from typing import Type

from slither.detectors import all_detectors as slither_all_detectors
from slither.detectors.abstract_detector import AbstractDetector

from sother.core.models import DetectorWiki
from sother.detectors.attributes.incorrect_solc import IncorrectSolc
from sother.detectors.dependency.chainlink import (
    DeprecatedChainLink,
    IgnoredChainlinkReturns,
    UncheckedChainlinkStaleness,
    UncheckedChainlinkRound,
)
from sother.detectors.dependency.unsafe_solmate_transfer_lib import (
    UnsafeSolmateTransferLib,
)
from sother.detectors.erc.erc20.deprecated_approve import DeprecatedApprove
from sother.detectors.erc.erc20.deprecated_safe_approve import DeprecatedSafeApprove
from sother.detectors.erc.erc20.revert_on_approve_max import RevertOnApproveMax
from sother.detectors.erc.erc20.revert_on_total_supply import RevertOnTotalSupply
from sother.detectors.erc.erc721.missing_erc721_received import (
    MissingErc721Received,
    UncheckedErc721Received,
)
from sother.detectors.erc.erc721.missing_supports_interface import (
    MissingSupportsInterface,
)
from sother.detectors.erc.erc721.non_compliant_erc721 import NonCompliantErc721
from sother.detectors.erc.erc721.unchecked_token_id import UncheckedTokenId
from sother.detectors.erc.erc721.unprotected_nft_fork import UnprotectedNFTFork
from sother.detectors.erc.erc721.unsafe_721_mint import Unsafe721Mint
from sother.detectors.erc.erc721.unsafe_721_transfer import UnsafeTransferErc721
from sother.detectors.events.missing_sender_in_event import MissingSenderInEvent
from sother.detectors.events.superfluous_fields_event import SuperfluousFieldsEvent
from sother.detectors.events.unindexed_event import UnindexedEvent
from sother.detectors.functions.cache_call_function_result import (
    CacheCallFunctionResult,
)
from sother.detectors.functions.dead_code import DeadCode
from sother.detectors.functions.external_function import ExternalFunction
from sother.detectors.functions.internal_function_to_inline import (
    InternalFunctionToInline,
)
from sother.detectors.functions.memory_in_parameters import MemoryInParameters
from sother.detectors.functions.payable_functions import (
    PayableConstructor,
    PayableFunction,
)
from sother.detectors.operations.assignment_left_operation import (
    AssignmentLeftOperation,
)
from sother.detectors.operations.division_by_zero import DivisionByZero
from sother.detectors.operations.encode_packed import EncodePackedCollision
from sother.detectors.operations.external_calls_in_loop import ExternalCallsInLoop
from sother.detectors.operations.fee_on_transfer import FeeOnTransfer
from sother.detectors.operations.missing_zero_address_validation import (
    MissingZeroAddressValidation,
)
from sother.detectors.operations.payable_calls import PayableCalls
from sother.detectors.operations.pre_plusplus import PrePlusPlus
from sother.detectors.operations.unchecked_low_level_return_values import (
    UncheckedLowLevel,
)
from sother.detectors.operations.unchecked_setters import UncheckedSetters
from sother.detectors.operations.unchecked_transfer import UncheckedTransfer
from sother.detectors.operations.unsafe_casting import UnsafeDowncast, UnsafeDoubleCast
from sother.detectors.operations.unsafe_tx_origin import UnsafeTxOrigin
from sother.detectors.operations.unsigned_int_compare_zero import UnsignedIntCompareZero
from sother.detectors.operations.unsupported_decimals_token import (
    UnsupportedDecimalsToken,
)
from sother.detectors.operations.unused_return_values import UnusedReturnValues
from sother.detectors.operations.use_selfbalance import (
    UseSelfBalance,
    UseAssemblyBalance,
)
from sother.detectors.operations.use_shifting import DivideByConstant, MulPowerTwo
from sother.detectors.operations.zero_address_optimization import (
    ZeroAddressOptimization,
)
from sother.detectors.operations.zero_on_transfer import ZeroCheckWithTransfer
from sother.detectors.permissions.deprecated_ownable import DeprecatedOwnable
from sother.detectors.permissions.owner_centralization import OwnerCentralization
from sother.detectors.pragma.unsafe_assembly import UnsafeAssembly
from sother.detectors.pragma.unsafe_floating_pragma import UnsafeFloatingPragma
from sother.detectors.pragma.upgrade_to_latest import UpgradeToLatest
from sother.detectors.reentrancy.reentrancy_send_value import ReentrancySendValue
from sother.detectors.reentrancy.reentrancy_transfer import ReentrancyTransfer
from sother.detectors.source.open_todos import OpenTodos
from sother.detectors.source.safe_math_lib import SafeMathLib
from sother.detectors.statements.array_length_in_loop import ArrayLengthInLoop
from sother.detectors.statements.boolean_constant_equality import BooleanEquality
from sother.detectors.statements.calls_in_loop import MultipleCallsInLoop
from sother.detectors.statements.deprecated_assert import DeprecatedAssert
from sother.detectors.statements.empty_block import EmptyBlock
from sother.detectors.statements.fetch_storage_to_memory import FetchStorageToMemory
from sother.detectors.statements.incorrect_deadline import IncorrectDeadline
from sother.detectors.statements.incorrect_strict_equality import (
    IncorrectStrictEquality,
)
from sother.detectors.statements.inefficient_new_bytes import InefficientNewBytes
from sother.detectors.statements.operator_and_in_require import OperatorAndInRequire
from sother.detectors.statements.revert_long_strings import RevertLongStrings
from sother.detectors.statements.susceptible_ecrecover import (
    SusceptibleEcrecover,
    UncheckedEcrecover,
)
from sother.detectors.statements.too_many_digits import TooManyDigits
from sother.detectors.statements.unchecked_array_length import UncheckedArrayLength
from sother.detectors.statements.unchecked_in_loop import UncheckedInLoop
from sother.detectors.statements.use_concat import UseConcatOnString, UseConcatOnBytes
from sother.detectors.statements.use_delete_statement import UseDeleteStatement
from sother.detectors.statements.used_custom_error import UsedCustomError
from sother.detectors.upgradeable.missing_gap_state_variable import (
    MissingGapStateVariable,
)
from sother.detectors.upgradeable.unprotected_upgradeable_front_run import (
    UnprotectedUpgradeableFrontRun,
)
from sother.detectors.upgradeable.unused_upgradeable_counterparts import (
    UnusedUpgradeableCounterparts,
)
from sother.detectors.upgradeable.upgradeable_uninitialized import (
    UpgradeableUninitialized,
)
from sother.detectors.variables.address_optimization import AssemblyUpdateAddress
from sother.detectors.variables.bool_state_variables import BoolStateVariables
from sother.detectors.variables.constants_optimization import (
    StringConstants,
    CalculateConstants,
    KeccakConstants,
    KeccakConstantInFunctions,
)
from sother.detectors.variables.could_be_immutable import CouldBeImmutable
from sother.detectors.variables.multiple_address_mappings import MultipleAddressMappings
from sother.detectors.variables.public_to_private_constant import (
    PublicToPrivateConstant,
)
from sother.detectors.variables.reread_state_variables import RereadStateVariables
from sother.detectors.variables.smaller_uint_int import SmallerUintInt
from sother.detectors.variables.uninitialized_local_variables import (
    UninitializedLocalVars,
)
from sother.detectors.variables.uninitialized_state_variables import (
    UninitializedStateVarsDetection,
)
from sother.detectors.variables.unused_variables import (
    UnusedStateVars,
    UnusedNamedReturnVariables,
    UnusedParameter,
    UnusedLocalVar,
    UnusedStruct,
    UnusedError,
)
from sother.detectors.variables.zero_initialized_state_variable import (
    ZeroInitializedStateVariable,
)


# from slither_pess import make_plugin as press_make_plugin


def extend_detectors(
    original_detectors: list[Type[AbstractDetector]],
    new_detectors: list[Type[AbstractDetector]],
) -> list[Type[AbstractDetector]]:
    detector_names = [
        item.__name__ for item in original_detectors if inspect.isclass(item)
    ]
    for detector in new_detectors:
        # if sother has override slither class, do not append slither class
        if inspect.isclass(detector) and detector.__name__ not in detector_names:
            original_detectors.append(detector)
            detector_names.append(detector.__name__)
    return original_detectors


def get_all_detectors() -> list[Type[AbstractDetector]]:
    detectors_ = get_detectors()
    # detectors_ = extend_detectors(detectors_, press_make_plugin()[0])
    detectors_ = extend_detectors(
        detectors_,
        [getattr(slither_all_detectors, name) for name in dir(slither_all_detectors)],
    )

    return [
        d for d in detectors_ if inspect.isclass(d) and issubclass(d, AbstractDetector)
    ]


def get_all_detector_wikis() -> dict[str, DetectorWiki]:
    detectors_list = sorted(
        get_all_detectors(),
        key=lambda element: (
            element.IMPACT,
            element.CONFIDENCE,
            element.ARGUMENT,
        ),
    )
    wikis = dict()
    for detector in detectors_list:
        wikis[detector.ARGUMENT] = DetectorWiki(
            argument=detector.ARGUMENT,
            help=detector.HELP,
            impact=detector.IMPACT,
            confidence=detector.CONFIDENCE,
            wiki=detector.WIKI,
            wiki_title=detector.WIKI_TITLE,
            wiki_description=detector.WIKI_DESCRIPTION,
            wiki_exploit_scenario=detector.WIKI_EXPLOIT_SCENARIO,
            wiki_recommendation=detector.WIKI_RECOMMENDATION,
        )
    return wikis


def get_detectors() -> list[Type[AbstractDetector]]:
    return [
        CouldBeImmutable,
        BoolStateVariables,
        FetchStorageToMemory,
        UpgradeToLatest,
        IncorrectSolc,
        AssignmentLeftOperation,
        InternalFunctionToInline,
        ArrayLengthInLoop,
        UncheckedInLoop,
        UsedCustomError,
        SmallerUintInt,
        PublicToPrivateConstant,
        RereadStateVariables,
        UnusedStateVars,
        UnusedNamedReturnVariables,
        UnusedParameter,
        UnusedLocalVar,
        UnusedStruct,
        UnusedError,
        DivideByConstant,
        MulPowerTwo,
        SuperfluousFieldsEvent,
        CacheCallFunctionResult,
        SafeMathLib,
        DeadCode,
        UnindexedEvent,
        OperatorAndInRequire,
        MemoryInParameters,
        UncheckedTransfer,
        PayableCalls,
        UncheckedArrayLength,
        DeprecatedAssert,
        ExternalCallsInLoop,
        UnprotectedUpgradeableFrontRun,
        MissingGapStateVariable,
        UpgradeableUninitialized,
        DeprecatedOwnable,
        DeprecatedSafeApprove,
        DeprecatedApprove,
        UnsafeTransferErc721,
        Unsafe721Mint,
        EncodePackedCollision,
        FeeOnTransfer,
        ZeroCheckWithTransfer,
        UninitializedLocalVars,
        UninitializedStateVarsDetection,
        UnusedReturnValues,
        ZeroAddressOptimization,
        PayableConstructor,
        PayableFunction,
        PrePlusPlus,
        UnsignedIntCompareZero,
        ZeroInitializedStateVariable,
        StringConstants,
        CalculateConstants,
        KeccakConstants,
        KeccakConstantInFunctions,
        RevertLongStrings,
        AssemblyUpdateAddress,
        ExternalFunction,
        UnsafeAssembly,
        BooleanEquality,
        EmptyBlock,
        MultipleAddressMappings,
        UnsafeDowncast,
        UnsafeDoubleCast,
        SusceptibleEcrecover,
        UncheckedEcrecover,
        UncheckedSetters,
        RevertOnApproveMax,
        UnsupportedDecimalsToken,
        UnsafeTxOrigin,
        UncheckedLowLevel,
        ReentrancySendValue,
        UnsafeFloatingPragma,
        UnsafeSolmateTransferLib,
        MissingSenderInEvent,
        UnprotectedNFTFork,
        UnusedUpgradeableCounterparts,
        UncheckedTokenId,
        MissingSupportsInterface,
        NonCompliantErc721,
        MissingErc721Received,
        UncheckedErc721Received,
        OpenTodos,
        UseSelfBalance,
        UseAssemblyBalance,
        UseDeleteStatement,
        InefficientNewBytes,
        DeprecatedChainLink,
        IgnoredChainlinkReturns,
        UncheckedChainlinkStaleness,
        UncheckedChainlinkRound,
        RevertOnTotalSupply,
        IncorrectDeadline,
        ReentrancyTransfer,
        UseConcatOnString,
        UseConcatOnBytes,
        DivisionByZero,
        MissingZeroAddressValidation,
        MultipleCallsInLoop,
        TooManyDigits,
        IncorrectStrictEquality,
        OwnerCentralization,
    ]


if __name__ == "__main__":
    unittest.main()
