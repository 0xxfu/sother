"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from slither.detectors.abstract_detector import DETECTOR_INFO, DetectorClassification
from slither.detectors.statements.unprotected_upgradeable import (
    UnprotectedUpgradeable as SlitherUnprotectedUpgradeable,
    _has_initializing_protection,
    _can_be_destroyed,
    _initialize_functions,
)
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


# todo except: onlyOwner onlyRole?
class UnprotectedUpgradeableFrontRun(SlitherUnprotectedUpgradeable):
    ARGUMENT = "unprotected-upgrade-front-run"
    HELP = (
        "Use `disableInitializers` to prevent front-running on the initialize function"
    )
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = (
        "Use `disableInitializers` to prevent front-running on the initialize function"
    )
    WIKI_DESCRIPTION = """
The implementation contracts behind a proxy can be initialized by any address. This is not a security problem in the sense that it impacts the system directly, as the attacker will not be able to cause any contract to self-destruct or modify any values in the proxy contracts. However, taking ownership of implementation contracts can open other attack vectors, like social engineering or phishing attacks.

More detail see [this OpenZeppelin docs](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#initializing_the_implementation_contract) and [this](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/62e2b8811b3cd80eb189aee7ae6764e937f8647b/contracts/proxy/utils/Initializable.sol#L47).
"""

    WIKI_EXPLOIT_SCENARIO = """ """

    WIKI_RECOMMENDATION = """
Use [disableInitializers](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/62e2b8811b3cd80eb189aee7ae6764e937f8647b/contracts/proxy/utils/Initializable.sol#L150-L165) 
to prevent front-running on the initialize function, as it would make you deploy the smart contract 
again if someone initializes it before you.

```
    constructor(){
        _disableInitializers();
    }
```

"""

    def _detect(self) -> List[Output]:
        results = []

        for contract in self.compilation_unit.contracts_derived:
            if contract.is_upgradeable:
                if not _has_initializing_protection(contract.constructors):
                    functions_that_can_destroy = _can_be_destroyed(contract)
                    if not functions_that_can_destroy:
                        initialize_functions = _initialize_functions(contract)

                        vars_init_ = [
                            init.all_state_variables_written()
                            for init in initialize_functions
                        ]
                        vars_init = [item for sublist in vars_init_ for item in sublist]

                        vars_init_in_constructors_ = [
                            f.all_state_variables_written()
                            for f in contract.constructors
                        ]
                        vars_init_in_constructors = [
                            item
                            for sublist in vars_init_in_constructors_
                            for item in sublist
                        ]
                        if vars_init and (
                            set(vars_init) - set(vars_init_in_constructors)
                        ):
                            info: DETECTOR_INFO = [
                                contract,
                                " is an upgradeable contract that does not protect its initialize functions: ",
                            ]
                            info += initialize_functions

                            res = self.generate_result(info)
                            results.append(res)
        return results


if __name__ == "__main__":
    unittest.main()
