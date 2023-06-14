"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from slither.core.variables import StateVariable
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
)
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class BoolStateVariables(AbstractDetector):
    ARGUMENT = "bool-state-variables"
    HELP = "Using `bool` replace `uint256(1)` and `uint256(2)` for true/false"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = (
        "Using `bool` replace `uint256(1)` and `uint256(2)` for true/false"
    )
    WIKI_DESCRIPTION = """
```solidity
// Booleans are more expensive than uint256 or any type that takes up a full
// word because each write operation emits an extra SLOAD to first read the
// slot's contents, replace the bits taken up by the boolean, and then write
// back. This is the compiler's defense against contract upgrades and
// pointer aliasing, and it cannot be disabled.

// The values being non-zero value makes deployment a bit more expensive,
// but in exchange the refund on every call to nonReentrant will be lower in
// amount. Since refunds are capped to a percentage of the total
// transaction's gas, it is best to keep them low in cases like this one, to
// increase the likelihood of the full refund coming into effect.
```
more detail see [this](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/58f635312aa21f947cae5f8578638a85aa2519f5/contracts/security/ReentrancyGuard.sol#L23-L33)
    
    """

    WIKI_RECOMMENDATION = "Use `uint256(1)` and `uint256(2)` for true/false to avoid a Gwarmaccess (**[100 gas](https://gist.github.com/0xxfu/d12e22af63cd2e0e9d6a8550360b2959)**) for the extra SLOAD, and to avoid Gsset (**20000 gas**) when changing from `false` to `true`, after having been `true` in the past"

    def _detect(self) -> List[Output]:
        results = []
        bool_state_variables: list[StateVariable] = []
        for contract in self.compilation_unit.contracts_derived:
            state_variables: list[StateVariable] = contract.state_variables
            # todo detect bool in mapping and struct
            for state in state_variables:
                if str(state.type) == "bool":
                    bool_state_variables.append(state)
        for bool_state in bool_state_variables:
            json = self.generate_result(
                [
                    "bool state ",
                    bool_state,
                    " should be replaced by `uint256(1)` and `uint256(2)`",
                ]
            )
            results.append(json)

        return results


if __name__ == "__main__":
    unittest.main()
