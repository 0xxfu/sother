"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List, Optional

from loguru import logger
from slither.core.declarations import Event
from slither.core.solidity_types import ElementaryType
from slither.core.variables.event_variable import EventVariable
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class UnindexedEvent(AbstractDetector):
    ARGUMENT = "unindexed-event"
    HELP = "Use indexed events for value types as they are less costly compared to non-indexed ones"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Use indexed events for value types as they are less costly compared to non-indexed ones"
    WIKI_DESCRIPTION = """
Using the `indexed` keyword for [value types](https://docs.soliditylang.org/en/v0.8.20/types.html#value-types) (`bool/int/address/string/bytes`) saves gas costs, as seen in [this example](https://gist.github.com/0xxfu/c292a65ecb61cae6fd2090366ea0877e).

However, this is only the case for value types, whereas indexing [reference types](https://docs.soliditylang.org/en/v0.8.20/types.html#reference-types) (`array/struct`) are more expensive than their unindexed version.
"""

    WIKI_RECOMMENDATION = """
Using the `indexed` keyword for values types `bool/int/address/string/bytes` in event
"""

    def _detect(self) -> List[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for event in contract.events:
                if event.name != "IntsEvent":
                    continue
                result_variables = self._detect_unindexed_event(event)
                if result_variables and len(result_variables) > 0:
                    logger.debug(
                        f"unindexed variables: {[var.name for var in result_variables]} in event: {event.name}"
                    )
                    result = [
                        "The following variables should be indexed in ",
                        event,
                        ":\n",
                    ]
                    for var in result_variables:
                        result += ["\n\t- ", var, "\n"]
                    res = self.generate_result(result)
                    results.append(res)

        return results

    @classmethod
    def _detect_unindexed_event(cls, event: Event) -> Optional[set[EventVariable]]:
        result_variables: set[EventVariable] = set()
        indexed = 0
        for var in event.elems:
            if var.indexed:
                indexed += 1
            logger.debug(f"var: {var.name} type: {type(var.type)}")
            if not isinstance(var.type, ElementaryType):
                continue
            if not var.indexed and indexed < 3:
                result_variables.add(var)
        if len(result_variables) <= 0:
            return None
        return result_variables


if __name__ == "__main__":
    unittest.main()
