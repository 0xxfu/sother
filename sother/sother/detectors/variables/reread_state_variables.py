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


def detect_reread_state(
    contract: Contract,
) -> dict[FunctionContract, dict[StateVariable, list[Node]]]:
    state_variable_reads: list[StateVariable] = contract.state_variables

    result_nodes: dict[FunctionContract, dict[StateVariable, list[Node]]] = dict()
    for function in contract.functions:
        if function.visibility == "external" and (function.view or function.pure):
            continue
        func_state_reads: [StateVariable, list[Node]] = dict()
        for node in function.nodes:
            node_state_reads = node.state_variables_read
            node_state_written = node.state_variables_written
            if len(node_state_written) <= 0:
                for state_read in node_state_reads:
                    if state_read not in state_variable_reads:
                        continue
                    if state_read not in func_state_reads:
                        func_state_reads[state_read] = []
                    func_state_reads[state_read].append(node)

            else:
                for state_written in node_state_written:
                    if state_written not in state_variable_reads:
                        continue
                    if (
                        state_written in func_state_reads
                        and len(func_state_reads[state_written]) <= 1
                    ):
                        func_state_reads[state_written] = []

        for state_read in func_state_reads:
            if len(func_state_reads[state_read]) > 1:
                if function not in result_nodes:
                    result_nodes[function] = dict()
                result_nodes[function][state_read] = func_state_reads[state_read]
    return result_nodes


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
            # dict: function -> state -> list[node]
            result_nodes = detect_reread_state(contract)
            for func in result_nodes:
                logger.debug(f"reread state: {func} {result_nodes[func]}")
                for state_read_in_func in result_nodes[func]:
                    result = [
                        state_read_in_func,
                        " should be cached with local memory-based variable in ",
                        func,
                        ", It is called more than once:\n",
                    ]
                    for node in result_nodes[func][state_read_in_func]:
                        result += ["\t- ", node, "\n"]
                    res = self.generate_result(result)
                    results.append(res)

        return results


if __name__ == "__main__":
    unittest.main()
