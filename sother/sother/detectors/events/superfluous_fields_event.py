"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from loguru import logger
from slither.analyses.data_dependency.data_dependency import is_dependent
from slither.core.cfg.node import Node
from slither.core.declarations import SolidityVariableComposed
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.slithir.operations import EventCall
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings
from sother.utils.gas_utils import GasUtils


# todo bug: except binary operation: block.number - request.blockNumber
class SuperfluousFieldsEvent(AbstractDetector):
    ARGUMENT = "superfluous-fields-event"
    HELP = "Superfluous fields in event"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Superfluous fields in event"
    WIKI_DESCRIPTION = """
`block.timestamp` and `block.number` are added to event information by default so adding them manually wastes gas
"""

    WIKI_RECOMMENDATION = """
Remove default fields(`block.timestamp` or `block.number`) in event.
"""

    def _detect(self) -> List[Output]:
        results = []
        result_nodes: set[Node] = set()
        for function in GasUtils.get_available_functions(self.compilation_unit):
            for node in function.nodes:
                for ir in node.all_slithir_operations():
                    if not isinstance(ir, EventCall):
                        continue
                    for var_read in ir.read:
                        if is_dependent(
                            var_read, SolidityVariableComposed("block.timestamp"), node
                        ):
                            result_nodes.add(node)
                        if is_dependent(
                            var_read, SolidityVariableComposed("block.number"), node
                        ):
                            result_nodes.add(node)

        for node in result_nodes:
            logger.debug(f"superfluous field: {node.expression}")
            res = self.generate_result(
                [
                    node,
                    " remove default fields(`block.timestamp` or `block.number`) in event to save gas.\n",
                ]
            )
            results.append(res)

        return results


if __name__ == "__main__":
    unittest.main()
