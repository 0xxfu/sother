"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.core.solidity_types import MappingType
from slither.core.variables import StateVariable
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class MultipleAddressMappings(AbstractDetector):
    ARGUMENT = "multiple-address-mappings"
    HELP = "Multiple address `mappings` can be combined into a single `mapping`"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Multiple address `mappings` can be combined into a single `mapping`"

    WIKI_DESCRIPTION = """
Saves a storage slot for the `mapping`. 
Depending on the circumstances and sizes of types, 
can avoid a `Gsset` (20000 gas) per `mapping` combined. Reads and subsequent writes can also 
be cheaper when a function requires both values and they both fit in the same storage slot. 
Finally, if both fields are accessed in the same function, can save `~42 gas` per access 
due to not having to recalculate the key’s `keccak256` hash (Gkeccak256 - 30 gas) and 
that calculation’s associated stack operations.
"""
    WIKI_RECOMMENDATION = """
Multiple address `mappings` can be combined into a single mapping of 
an address to a struct, where appropriate.
"""

    def _detect(self) -> list[Output]:
        results = []
        for contract in self.compilation_unit.contracts_derived:
            type_mappings: dict[str, set[StateVariable]] = dict()
            for var in contract.state_variables_declared:
                var_t = var.type
                if not isinstance(var_t, MappingType):
                    continue
                mapping_key_type = str(var_t.type_from)
                if str(mapping_key_type) not in type_mappings:
                    type_mappings[mapping_key_type] = set()
                type_mappings[mapping_key_type].add(var)

            for t_mapping in type_mappings:
                mapping_list = type_mappings[t_mapping]
                if len(mapping_list) > 1:
                    info: DETECTOR_INFO = [
                        "Following mappings should be combined into one:\n",
                    ]
                    for state in sorted(
                        mapping_list, key=lambda x: x.source_mapping.lines[0]
                    ):
                        info += [f"\t- ", state, "\n"]

                    res = self.generate_result(info)
                    results.append(res)

        return results


if __name__ == "__main__":
    unittest.main()
