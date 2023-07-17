"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import abc
import unittest
from abc import ABC
from typing import Optional

from loguru import logger
from slither.analyses.data_dependency.data_dependency import is_dependent
from slither.core.cfg.node import Node
from slither.core.declarations import Function, FunctionContract
from slither.core.expressions import AssignmentOperation
from slither.core.variables.local_variable import LocalVariable
from slither.detectors.abstract_detector import DETECTOR_INFO, DetectorClassification
from slither.slithir.operations import Operation, HighLevelCall, Unpack, InternalCall

from sother.detectors.abstracts.abstract_detect_has_instance import (
    AbstractDetectHasInstance,
)
from sother.detectors.detector_settings import DetectorSettings


class DeprecatedChainLink(AbstractDetectHasInstance):
    ARGUMENT = "deprecated-chainlink"
    HELP = "Usage of deprecated ChainLink APIs"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Usage of deprecated ChainLink APIs"

    WIKI_DESCRIPTION = """
According to [Chainlink's documentation](https://docs.chain.link/data-feeds/api-reference),
the following functions are deprecated: `latestRound()`/`latestAnswer()`/`latestTimestamp()`/
`getAnswer(uint256 _roundId)`/`getTimestamp(uint256 _roundId)`. 

> This does not error if no
> answer has been reached, it will simply return 0. Either wait to point to
> an already answered Aggregator or use the recommended `getRoundData`
> instead which includes better verification information.

Impact: Deprecated API stops working. 
Prices cannot be obtained. Protocol stops and contracts have to be redeployed.
"""

    WIKI_RECOMMENDATION = """
It is recommended to use `latestRoundData()` method instead of deprecated APIs.
"""

    WIKI_EXPLOIT_SCENARIO = " "

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        return (
            isinstance(ir, HighLevelCall)
            and isinstance(ir.function, Function)
            and ir.function.solidity_signature
            in [
                "latestRound()",
                "latestAnswer()",
                "latestTimestamp()",
                "getAnswer(uint256)",
                "getTimestamp(uint256)",
            ]
        )

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            " should use `latestRoundData()` instead of ",
            node,
            "\n",
        ]


class AbstractUncheckedChainlink(AbstractDetectHasInstance, ABC):
    return_size = 5

    @classmethod
    @abc.abstractmethod
    def _is_unchecked_instance(
        cls, ir: Operation, local_var_written: list[LocalVariable]
    ) -> bool:
        pass

    @classmethod
    def _is_instance(cls, ir: Operation) -> bool:
        if (
            isinstance(ir, HighLevelCall)
            and isinstance(ir.function, Function)
            and ir.function.solidity_signature
            in [
                "latestRoundData()",
            ]
        ):
            return cls._is_unchecked_instance(ir, ir.node.local_variables_written)
        return False

    @classmethod
    def _is_checked_variable(
        cls, local_var: LocalVariable, nodes: list[Node], visited: list[Node] = None
    ) -> bool:
        if visited is None:
            visited = list()
        for node in nodes:
            if node.contains_require_or_assert() or node.contains_if():
                for var in node.local_variables_read:
                    if is_dependent(var, local_var, node):
                        return True
            else:
                for ir in node.irs:
                    if isinstance(ir, InternalCall) and isinstance(
                        ir.function, FunctionContract
                    ):
                        if cls._is_checked_variable(
                            local_var, ir.function.nodes, visited
                        ):
                            return True
        return False

    @classmethod
    def _get_unpack_written_variable(
        cls, unpack_index, node: Node
    ) -> Optional[LocalVariable]:
        unpack_idx = 0
        local_var_written: Optional[LocalVariable] = None
        for node_ir in node.irs:
            if isinstance(node_ir, Unpack):
                if unpack_idx == unpack_index:
                    local_var_written = node_ir.lvalue
                unpack_idx += 1
        return local_var_written


class IgnoredChainlinkReturns(AbstractUncheckedChainlink):
    ARGUMENT = "ignored-chainlink-returns"
    HELP = "`latestRoundData` returns has been ignored"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki
    WIKI_TITLE = "`latestRoundData` returns has been ignored"

    WIKI_DESCRIPTION = """
The `latestRoundData` function in the contract `xxx.sol` fetches the asset price 
from a Chainlink aggregator using the latestRoundData function. 
However, the returns is ignored.

If there is a problem with chainlink starting a new round and finding consensus 
on the new value for the oracle (e.g. chainlink nodes abandon the oracle, 
chain congestion, vulnerability/attacks on the chainlink system) 
consumers of this contract may continue using outdated stale data 
(if oracles are unable to submit no new round is started)

"""

    WIKI_RECOMMENDATION = """
Consider checking the all oracle responses value after calling out 
to `chainlinkOracle.latestRoundData()` verifying that the result is within 
an allowed margin.

For example:
```
    (
        uint80 roundId,
        int256 price,
        uint256 startedAt,
        uint256 updatedAt,
        uint80 answeredInRound
    ) = aggregator.latestRoundData();

    if (updatedAt < roundId) {
        revert("Stale price");
    }
    if (answeredInRound < roundId){
        revert("answer is being carried over");
    }
    if (startedAt == 0) {
        revert("Round not complete");
    }
    if (price == 0) {
        revert("answer reporting 0");
    }

    if (updatedAt < block.timestamp - maxDelayTime) {
        revert("time err");
    }
```
"""

    WIKI_EXPLOIT_SCENARIO = " "

    @classmethod
    def _is_unchecked_instance(
        cls, ir: Operation, local_var_written: list[LocalVariable]
    ) -> bool:
        return len(local_var_written) < cls.return_size

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            node,
            " returns has been ignored.",
            "\n",
        ]


class UncheckedChainlinkStaleness(AbstractUncheckedChainlink):
    ARGUMENT = "unchecked-chainlink-staleness"
    HELP = "`latestRoundData` might return stale results"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki
    WIKI_TITLE = "`latestRoundData` might return stale results"

    WIKI_DESCRIPTION = """
The `latestRoundData` function in the contract `xxx.sol` fetches the asset price 
from a Chainlink aggregator using the latestRoundData function. 
However, the returns `updatedAt` timestamp is not checked.

If there is a problem with chainlink starting a new round and finding consensus 
on the new value for the oracle (e.g. chainlink nodes abandon the oracle, 
chain congestion, vulnerability/attacks on the chainlink system) 
consumers of this contract may continue using outdated stale data 
(if oracles are unable to submit no new round is started)

"""

    WIKI_RECOMMENDATION = """
Consider checking the oracle responses `updatedAt` value after calling out 
to `chainlinkOracle.latestRoundData()` verifying that the result is within 
an allowed margin of freshness.

For example:
```
    (
        uint80 roundId,
        int256 price,
        uint256 startedAt,
        uint256 updatedAt,
        uint80 answeredInRound
    ) = aggregator.latestRoundData();

    if (updatedAt < roundId) {
        revert("Stale price");
    }
    if (answeredInRound < roundId){
        revert("answer is being carried over");
    }
    if (startedAt == 0) {
        revert("Round not complete");
    }
    if (price == 0) {
        revert("answer reporting 0");
    }

    if (updatedAt < block.timestamp - maxDelayTime) {
        revert("time err");
    }
```
"""

    WIKI_EXPLOIT_SCENARIO = " "

    @classmethod
    def _is_unchecked_instance(
        cls, ir: Operation, local_vars_written: list[LocalVariable]
    ) -> bool:
        if len(local_vars_written) < cls.return_size:
            return False

        unpack_index = 3
        local_var_written: Optional[LocalVariable] = cls._get_unpack_written_variable(
            unpack_index, ir.node
        )

        if local_var_written is None:
            return False

        return not cls._is_checked_variable(local_var_written, ir.node.sons)

    @classmethod
    def _detect_node_info(cls, node: Node) -> DETECTOR_INFO:
        return [
            node,
            " unchecked `updatedAt` of `latestRoundData()`.",
            "\n",
        ]


if __name__ == "__main__":
    unittest.main()
