## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Lack of a double-step `transferOwnership()` pattern | 3 |
| [L-1] | Upgradeable contract is missing a `__gap` storage variable to allow for new storage variables in later versions | 2 |
| [L-2] | Upgradeable contracts are not initialized | 2 |
| [L-3] | Missing zero address validation | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | use custom errors instead of revert strings | 3 |



## [Low] Lack of a double-step `transferOwnership()` pattern

### description:

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



**There are `3` instances of this issue:**

- [DeprecatedOwnable](solidity/test_deprecated_ownable.sol#L9) does not implement a `2-Step-Process` for transferring ownership.
- [DeprecatedOwnableUpgradeable](solidity/test_deprecated_ownable.sol#L11) does not implement a `2-Step-Process` for transferring ownership.
- [DeprecatedTransferOwnerShip](solidity/test_deprecated_ownable.sol#L13-L41) does not implement a `2-Step-Process` for transferring ownership.

### recommendation:

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


### locations:
- solidity/test_deprecated_ownable.sol#L9
- solidity/test_deprecated_ownable.sol#L11
- solidity/test_deprecated_ownable.sol#L13-L41

### severity:
Low

### category:
deprecated-ownable

## [Low] Upgradeable contract is missing a `__gap` storage variable to allow for new storage variables in later versions

### description:

See [this](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#storage-gaps) link for a description of this storage variable. While some contracts may not currently be sub-classed, adding the variable now protects against forgetting to add it in the future.



**There are `2` instances of this issue:**

- [OwnableUpgradeable](solidity/test_deprecated_ownable.sol#L7) is an upgradeable contract that miss `__gap` to allow for new storage variables.
- [DeprecatedOwnableUpgradeable](solidity/test_deprecated_ownable.sol#L11) is an upgradeable contract that miss `__gap` to allow for new storage variables.

### recommendation:

It is considered a best practice in upgradeable contracts to include a
state variable named `__gap`. This `__gap` state variable will be used as a
reserved space for future upgrades. It allows adding new state variables
freely in the future without compromising the storage compatibility with
existing deployments.
The size of the __gap array is usually calculated so that the amount of
storage used by a contract always adds up to the same number (usually 50
storage slots).

```
contract Contract {
    ...
    
    # declare `__gap` variable at the end of all states
    uint256[50] private __gap;
}
```



### locations:
- solidity/test_deprecated_ownable.sol#L7
- solidity/test_deprecated_ownable.sol#L11

### severity:
Low

### category:
missing-gap-state-variable

## [Low] Upgradeable contracts are not initialized

### description:

Upgradeable contracts are initialized via an initializer function rather than by a constructor. 
Leaving such a contract uninitialized may lead to it being taken over by a malicious user


**There are `2` instances of this issue:**

- [OwnableUpgradeable](solidity/test_deprecated_ownable.sol#L7) is an upgradeable contract that does not initialized
- [DeprecatedOwnableUpgradeable](solidity/test_deprecated_ownable.sol#L11) is an upgradeable contract that does not initialized

### recommendation:

Consider initializing function in the related section.

```
contract Contract {
    ...
    # 
    function initialize() public initializer {
        OwnableUpgradeable.__Ownable_init();
        __ReentrancyGuard_init();
    }

}
```


### locations:
- solidity/test_deprecated_ownable.sol#L7
- solidity/test_deprecated_ownable.sol#L11

### severity:
Low

### category:
upgradeable-uninitialized

## [Low] Missing zero address validation

### description:
Detect missing zero address validation.

**There is `1` instance of this issue:**

- [DeprecatedTransferOwnerShipFixed.transferOwnership(address).newOwner](solidity/test_deprecated_ownable.sol#L46) lacks a zero-check on :
		- [_pendingOwner = newOwner](solidity/test_deprecated_ownable.sol#L52)

#### Exploit scenario

```solidity
contract C {

  modifier onlyAdmin {
    if (msg.sender != owner) throw;
    _;
  }

  function updateOwner(address newOwner) onlyAdmin external {
    owner = newOwner;
  }
}
```
Bob calls `updateOwner` without specifying the `newOwner`, so Bob loses ownership of the contract.


### recommendation:
Check that the address is not zero.

### locations:
- solidity/test_deprecated_ownable.sol#L46

### severity:
Low

### category:
missing-zero-check

## [Informational] Incorrect versions of Solidity

### description:

`solc` frequently releases new compiler versions. Using an old version prevents access to new Solidity security checks.
We also recommend avoiding complex `pragma` statement.

**There is `1` instance of this issue:**

- solc-0.8.19 is not recommended for deployment


### recommendation:

Deploy with any of the following Solidity versions:
- 0.8.20

The recommendations take into account:
- Risks related to recent releases
- Risks of complex code generation changes
- Risks of new language features
- Risks of known bugs

Use a simple pragma version that allows any of these versions.
Consider using the latest version of Solidity for testing.

### locations:
- 

### severity:
Informational

### category:
solc-version

## [Optimization] use custom errors instead of revert strings

### description:

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `3` instances of this issue:**

- [require(bool,string)(_owner == msg.sender,Ownable: caller is not the owner)](solidity/test_deprecated_ownable.sol#L25) should use custom error to save gas.

- [require(bool,string)(newOwner != address(0),Ownable: new owner is the zero address)](solidity/test_deprecated_ownable.sol#L29-L32) should use custom error to save gas.

- [require(bool,string)(_pendingOwner == sender,Ownable2Step: caller is not the new owner)](solidity/test_deprecated_ownable.sol#L62-L65) should use custom error to save gas.


### recommendation:

Using custom errors replace `require` or `assert`.


### locations:
- solidity/test_deprecated_ownable.sol#L25
- solidity/test_deprecated_ownable.sol#L29-L32
- solidity/test_deprecated_ownable.sol#L62-L65

### severity:
Optimization

### category:
use-custom-error
