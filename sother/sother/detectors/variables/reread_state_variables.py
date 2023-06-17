"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.declarations import FunctionContract, Contract
from slither.core.variables import StateVariable
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


def detect_reread_state(contract: Contract) -> dict[FunctionContract, list[Node]]:
    state_variable_reads: dict[StateVariable, list[Node]] = dict()

    for state in contract.state_variables:
        state_variable_reads[state] = []
    logger.debug(f"state names: {state_variable_reads}")

    for function in contract.functions:
        if function.visibility == "external" and (function.view or function.pure):
            continue
        logger.debug(f"function: {function.name}")
        for node in function.nodes:
            logger.debug(
                f"node: {node.expression}\n"
                f"state read: {node.state_variables_read}\n"
                f"state written: {node.state_variables_written}\n"
            )
            node_state_reads = node.state_variables_read
            node_state_written = node.state_variables_written
            if len(node_state_written) <= 0:
                for state_read in node_state_reads:
                    if state_read not in state_variable_reads:
                        continue
                    state_variable_reads[state_read].append(node)

            else:
                for state_written in node_state_written:
                    if state_written.name not in state_variable_reads:
                        continue
                    if len(state_variable_reads[state_written]) <= 1:
                        state_variable_reads[state_written] = []
    result_states: dict[StateVariable, list[Node]] = dict()
    for state in state_variable_reads:
        if len(state_variable_reads[state]) > 1:
            result_states[state] = state_variable_reads[state]

    logger.debug(f"state reads: {result_states}")
    return result_states


class RereadStateVariables(AbstractDetector):
    ARGUMENT = "reread-state-variables"
    HELP = "State variables should be cached in stack variables rather than re-reading them from storage"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "State variables should be cached in stack variables rather than re-reading them from storage"
    WIKI_DESCRIPTION = """
The instances below point to the second+ access of a state variable within a function. Caching of a state variable replaces each Gwarmaccess (**100 gas**) with a much cheaper stack read. Other less obvious fixes/optimizations include having local memory caches of state variable structs, or having local caches of state variable contracts/addresses.

More detail see [this.](https://gist.github.com/0xxfu/af8f63ccbf36af9d067ed6eff9ff7129)
"""

    WIKI_RECOMMENDATION = """
Cache storage-based state variables in local memory-based variables appropriately to convert SLOADs to MLOADs and reduce gas consumption from 100 units to 3 units. than once for a function
"""

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            state_reads = detect_reread_state(contract)
            for state in state_reads:
                logger.debug(f"reread state: {state} {state_reads[state]}")
                result = []
                for item in state_reads[state]:
                    result.append(item)
                    result.append("  ")
                result += [
                    " more than once read data from state ",
                    state,
                    " should cache the state in local memory-based variable",
                ]
                res = self.generate_result(result)
                results.append(res)
        return results


if __name__ == "__main__":
    unittest.main()
