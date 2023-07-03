"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.solidity_types.elementary_type import Int, Uint
from slither.core.variables import Variable
from slither.detectors.abstract_detector import (
    DetectorClassification,
    AbstractDetector,
)
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings
from sother.utils.gas_utils import GasUtils


# todo detect uint/int in mapping and struct
class SmallerUintInt(AbstractDetector):
    ARGUMENT = "smaller-uint-int"
    HELP = "Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = (
        "Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead"
    )
    WIKI_DESCRIPTION = """
> When using elements that are smaller than 32 bytes, your contract’s gas usage may be higher. This is because the EVM operates on 32 bytes at a time. Therefore, if the element is smaller than that, the EVM must use more operations in order to reduce the size of the element from 32 bytes to the desired size.

More detail see [this.](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html)

Each operation involving a `uint8` costs an extra [**22-28 gas**](https://gist.github.com/0xxfu/3672fec07eb3031cd5da14ac015e04a1) (depending on whether the other operand is also a variable of type `uint8`) as compared to ones involving `uint256`, due to the compiler having to clear the higher bits of the memory word before operating on the `uint8`, as well as the associated stack operations of doing so. Use a larger size then downcast where needed
"""

    WIKI_RECOMMENDATION = """
Using `uint256/int256` replace `uint128/uint64/uint32/uint16/uint8` or `int128/int64/int32/int16/int8`
"""

    def _detect(self) -> List[Output]:
        results = []
        small_ints: list[Variable] = []
        small_types: list[str] = Int + Uint
        remove_types = ["uint256", "int256"]

        for remove_type in remove_types:
            if remove_type in small_types:
                small_types.remove(remove_type)

        for contract in self.compilation_unit.contracts:
            for state in contract.state_variables:
                if str(state.type) in small_types:
                    small_ints.append(state)
        for function in GasUtils.get_available_functions(self.compilation_unit):
            for variable in function.variables:
                if str(variable.type) in small_types:
                    small_ints.append(variable)

        for small_int in small_ints:
            res = self.generate_result(
                [
                    f"`{str(small_int.type)} `",
                    small_int,
                    " should be used `uint256/int256`.\n",
                ]
            )
            results.append(res)
        return results


if __name__ == "__main__":
    unittest.main()
