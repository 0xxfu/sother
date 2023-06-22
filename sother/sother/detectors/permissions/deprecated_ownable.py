"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List, Optional

from slither.core.declarations import Contract
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class DeprecatedOwnable(AbstractDetector):
    ARGUMENT = "deprecated-ownable"
    HELP = "Lack of a double-step `transferOwnership()` pattern"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Lack of a double-step `transferOwnership()` pattern"
    WIKI_DESCRIPTION = """
The current ownership transfer process for all the contracts inheriting
from `Ownable` or `OwnableUpgradeable` involves the current owner calling the
[transferOwnership()](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.8/contracts/access/Ownable.sol#L69-L72) function:

```
    function transferOwnership(address newOwner) public virtual onlyOwner {
        require(newOwner != address(0), "Ownable: new owner is the zero address");
        _transferOwnership(newOwner);
    }
```
If the nominated EOA account is not a valid account, it is entirely possible
that the owner may accidentally transfer ownership to an uncontrolled
account, losing the access to all functions with the `onlyOwner` modifier.

"""

    WIKI_RECOMMENDATION = """
It is recommended to implement a two-step process where the owner nominates
an account and the nominated account needs to call an `acceptOwnership()`
function for the transfer of the ownership to fully succeed. This ensures
the nominated EOA account is a valid and active account. This can be
easily achieved by using OpenZeppelin’s [Ownable2Step](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.8/contracts/access/Ownable2Step.sol) contract instead of
`Ownable`:

```
abstract contract Ownable2Step is Ownable {

    /**
     * @dev Starts the ownership transfer of the contract to a new account. Replaces the pending transfer if there is one.
     * Can only be called by the current owner.
     */
    function transferOwnership(address newOwner) public virtual override onlyOwner {
        _pendingOwner = newOwner;
        emit OwnershipTransferStarted(owner(), newOwner);
    }
    
    ...

    /**
     * @dev The new owner accepts the ownership transfer.
     */
    function acceptOwnership() external {
        address sender = _msgSender();
        require(pendingOwner() == sender, "Ownable2Step: caller is not the new owner");
        _transferOwnership(sender);
    }
}
```
"""
    WIKI_EXPLOIT_SCENARIO = " "

    @classmethod
    def _detect_owner_ship(cls, contract: Contract) -> Optional[Contract]:
        has_transfer_ownership = False
        has_accept_ownership = False
        for function in contract.functions_declared:
            if function.name == "transferOwnership":
                has_transfer_ownership = True
            elif function.name == "acceptOwnership":
                has_accept_ownership = True
        if has_transfer_ownership and not has_accept_ownership:
            return contract
        return None

    def _detect(self) -> List[Output]:
        results = []
        result_contracts: set[Contract] = set()

        deprecated_ownables: list[str] = ["Ownable", "OwnableUpgradeable"]
        for contract in self.compilation_unit.contracts:
            # inherit owneable
            if any(
                inherit.name in deprecated_ownables for inherit in contract.inheritance
            ):
                result_contracts.add(contract)

            # self implement ownership
            result = self._detect_owner_ship(contract)
            if result:
                result_contracts.add(contract)

        for result in result_contracts:
            info: DETECTOR_INFO = [
                result,
                " does not implement a `2-Step-Process` for transferring ownership.",
            ]
            res = self.generate_result(info)
            results.append(res)

        return results


if __name__ == "__main__":
    unittest.main()
