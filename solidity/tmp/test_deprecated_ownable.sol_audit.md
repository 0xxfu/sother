## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | The owner is a single point of failure and a centralization risk | 2 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Upgradeable contract is missing a `__gap` storage variable to allow for new storage variables in later versions | 2 |
| [L-1] | Upgradeable contracts are not initialized | 2 |
| [L-2] | Lack of a double-step `transferOwnership()` pattern | 3 |
| [L-3] | Missing zero address validation | 1 |
| [L-4] | Missing Event Setter | 3 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Unnecessary Public Function Modifier | 2 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Using custom errors replace `require` or `assert` | 3 |
| [G-1] | Use assembly to check for `address(0)` | 1 |
| [G-2] | Functions guaranteed to revert when called by normal users can be marked `payable` | 2 |
| [G-3] | Shortening revert strings to fit in 32 `bytes` | 2 |
| [G-4] | Use `assembly` to write address storage values | 4 |



## [Medium] The owner is a single point of failure and a centralization risk

### description

Having a single EOA as the only owner of contracts is a large centralization risk and a single point of failure. A single private key may be taken in a hack, or the sole holder of the key may become unable to retrieve the key when necessary.

There are several privileged entities that have access to sensitive operations as follows.


**There are `2` instances of this issue:**

- The role [DeprecatedTransferOwnerShip.onlyOwner()](solidity/tmp/test_deprecated_ownable.sol#L19-L22) is a single point of failure and a centralization risk. and have access to sensitive operations as follows:
	- [DeprecatedTransferOwnerShip.transferOwnership(address)](solidity/tmp/test_deprecated_ownable.sol#L28-L34)

- The role [DeprecatedTransferOwnerShip.onlyOwner()](solidity/tmp/test_deprecated_ownable.sol#L19-L22) is a single point of failure and a centralization risk. and have access to sensitive operations as follows:
	- [DeprecatedTransferOwnerShipFixed.transferOwnership(address)](solidity/tmp/test_deprecated_ownable.sol#L46-L53)


### recommendation

Add a time lock to critical functions. Admin-only functions that change critical parameters should emit events and have timelocks.
Events allow capturing the changed parameters so that off-chain tools/interfaces can register such changes with timelocks that allow users to evaluate them and consider if they would like to engage/exit based on how they perceive the changes as affecting the trustworthiness of the protocol or profitability of the implemented financial services.

Allow only multi-signature wallets to call the function to reduce the likelihood of an attack.


### locations
- solidity/tmp/test_deprecated_ownable.sol#L19-L22
- solidity/tmp/test_deprecated_ownable.sol#L19-L22

### severity
Medium

### category
owner-centralization

### confidence
High

## [Low] Upgradeable contract is missing a `__gap` storage variable to allow for new storage variables in later versions

### description

See [this](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#storage-gaps) link for a description of this storage variable. While some contracts may not currently be sub-classed, adding the variable now protects against forgetting to add it in the future.



**There are `2` instances of this issue:**

- [OwnableUpgradeable](solidity/tmp/test_deprecated_ownable.sol#L7) is an upgradeable contract that miss `__gap` to allow for new storage variables.
- [DeprecatedOwnableUpgradeable](solidity/tmp/test_deprecated_ownable.sol#L11) is an upgradeable contract that miss `__gap` to allow for new storage variables.

### recommendation

It is considered a best practice in upgradeable contracts to include a
state variable named `__gap`. This `__gap` state variable will be used as a
reserved space for future upgrades. It allows adding new state variables
freely in the future without compromising the storage compatibility with
existing deployments.
The size of the `__gap` array is usually calculated so that the amount of
storage used by a contract always adds up to the same number (usually 50
storage slots).

```
contract Contract {
    ...
    
    # declare `__gap` variable at the end of all states
    uint256[50] private __gap;
}
```



### locations
- solidity/tmp/test_deprecated_ownable.sol#L7
- solidity/tmp/test_deprecated_ownable.sol#L11

### severity
Low

### category
missing-gap-state-variable

### confidence
High

## [Low] Upgradeable contracts are not initialized

### description

Upgradeable contracts are initialized via an initializer function rather than by a constructor. 
Leaving such a contract uninitialized may lead to it being taken over by a malicious user


**There are `2` instances of this issue:**

- [OwnableUpgradeable](solidity/tmp/test_deprecated_ownable.sol#L7) is an upgradeable contract that does not initialized
- [DeprecatedOwnableUpgradeable](solidity/tmp/test_deprecated_ownable.sol#L11) is an upgradeable contract that does not initialized

### recommendation

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


### locations
- solidity/tmp/test_deprecated_ownable.sol#L7
- solidity/tmp/test_deprecated_ownable.sol#L11

### severity
Low

### category
upgradeable-uninitialized

### confidence
High

## [Low] Lack of a double-step `transferOwnership()` pattern

### description

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

- [DeprecatedOwnable](solidity/tmp/test_deprecated_ownable.sol#L9) does not implement a `2-Step-Process` for transferring ownership.
- [DeprecatedOwnableUpgradeable](solidity/tmp/test_deprecated_ownable.sol#L11) does not implement a `2-Step-Process` for transferring ownership.
- [DeprecatedTransferOwnerShip](solidity/tmp/test_deprecated_ownable.sol#L13-L41) does not implement a `2-Step-Process` for transferring ownership.

### recommendation

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


### locations
- solidity/tmp/test_deprecated_ownable.sol#L9
- solidity/tmp/test_deprecated_ownable.sol#L11
- solidity/tmp/test_deprecated_ownable.sol#L13-L41

### severity
Low

### category
deprecated-ownable

### confidence
High

## [Low] Missing zero address validation

### description
Missing zero address validation.

**There is `1` instance of this issue:**

- [DeprecatedTransferOwnerShipFixed.transferOwnership(address).newOwner](solidity/tmp/test_deprecated_ownable.sol#L46) lacks a zero-check on :
		- [_pendingOwner = newOwner](solidity/tmp/test_deprecated_ownable.sol#L52)

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


### recommendation
Check that the address is not zero.

### locations
- solidity/tmp/test_deprecated_ownable.sol#L46

### severity
Low

### category
missing-zero-check

### confidence
Medium

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `3` instances of this issue:**

- Setter function [DeprecatedTransferOwnerShipFixed.transferOwnership(address)](solidity/tmp/test_deprecated_ownable.sol#L46-L53) does not emit an event

- Setter function [DeprecatedTransferOwnerShipFixed._transferOwnership(address)](solidity/tmp/test_deprecated_ownable.sol#L55-L58) does not emit an event

- Setter function [DeprecatedTransferOwnerShipFixed.acceptOwnership()](solidity/tmp/test_deprecated_ownable.sol#L60-L67) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/test_deprecated_ownable.sol#L46-L53
- solidity/tmp/test_deprecated_ownable.sol#L55-L58
- solidity/tmp/test_deprecated_ownable.sol#L60-L67

### severity
Low

### category
pess-event-setter

### confidence
Medium

## [Informational] Incorrect versions of Solidity

### description

`solc` frequently releases new compiler versions. Using an old version prevents access to new Solidity security checks.
We also recommend avoiding complex `pragma` statement.

**There is `1` instance of this issue:**

- solc-0.8.17 is not recommended for deployment


### recommendation

Deploy with any of the following Solidity versions:
- 0.8.21

The recommendations take into account:
- Risks related to recent releases
- Risks of complex code generation changes
- Risks of new language features
- Risks of known bugs

Use a simple pragma version that allows any of these versions.
Consider using the latest version of Solidity for testing.

### locations
- 

### severity
Informational

### category
solc-version

### confidence
High

## [Informational] Unnecessary Public Function Modifier

### description
Detect the public function which can be replaced with external

**There are `2` instances of this issue:**

- function:[DeprecatedTransferOwnerShip.transferOwnership(address)](solidity/tmp/test_deprecated_ownable.sol#L28-L34)is public and can be replaced with external 

- function:[DeprecatedTransferOwnerShipFixed.transferOwnership(address)](solidity/tmp/test_deprecated_ownable.sol#L46-L53)is public and can be replaced with external 

#### Exploit scenario

```solidity
contract A{}
contract B is A{
    constructor() public A(){}
}
```
When reading `B`'s constructor definition, we might assume that `A()` initiates the contract, but no code is executed.

### recommendation
Replace public with external

### locations
- solidity/tmp/test_deprecated_ownable.sol#L28-L34
- solidity/tmp/test_deprecated_ownable.sol#L46-L53

### severity
Informational

### category
unnecessary-public-function-modifier

### confidence
High

## [Optimization] Using custom errors replace `require` or `assert`

### description

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `3` instances of this issue:**

- [require(bool,string)(_owner == msg.sender,"Ownable: caller is not the owner")](solidity/tmp/test_deprecated_ownable.sol#L25) should use custom error to save gas.

- [require(bool,string)(newOwner != address(0),"Ownable: new owner is the zero address")](solidity/tmp/test_deprecated_ownable.sol#L29-L32) should use custom error to save gas.

- [require(bool,string)(_pendingOwner == sender,"Ownable2Step: caller is not the new owner")](solidity/tmp/test_deprecated_ownable.sol#L62-L65) should use custom error to save gas.


### recommendation

Using custom errors replace `require` or `assert`.


### locations
- solidity/tmp/test_deprecated_ownable.sol#L25
- solidity/tmp/test_deprecated_ownable.sol#L29-L32
- solidity/tmp/test_deprecated_ownable.sol#L62-L65

### severity
Optimization

### category
use-custom-error

### confidence
High

## [Optimization] Use assembly to check for `address(0)`

### description

[Inline Assembly](https://docs.soliditylang.org/en/latest/assembly.html) more gas efficient and [Saving Gas with Simple Inlining](https://blog.soliditylang.org/2021/03/02/saving-gas-with-simple-inliner/).



**There is `1` instance of this issue:**

- [require(bool,string)(newOwner != address(0),"Ownable: new owner is the zero address")](solidity/tmp/test_deprecated_ownable.sol#L29-L32) should use assembly to check for `address(0)`


### recommendation

Use assembly to check for `address(0)`:

```
function addrNotZero(address _addr) public pure {
        assembly {
            if iszero(_addr) {
                mstore(0x00, "zero address")
                revert(0x00, 0x20)
            }
        }
}
```


### locations
- solidity/tmp/test_deprecated_ownable.sol#L29-L32

### severity
Optimization

### category
zero-address-optimization

### confidence
High

## [Optimization] Functions guaranteed to revert when called by normal users can be marked `payable`

### description

If a function modifier such as `onlyOwner/onlyAdmin/only**` is used, 
the function will revert if a normal user tries to pay the function. 
Marking the function as payable will lower the gas cost for legitimate callers 
because the compiler will not include checks for whether a payment was provided. 

The extra opcodes avoided are `CALLVALUE(2)`,`DUP1(3)`,`ISZERO(3)`,`PUSH2(3)`,
`JUMPI(10)`,`PUSH1(3)`,`DUP1(3)`,`REVERT(0)`,`JUMPDEST(1)`,`POP(2)`, 
which costs an average of about `21 gas` per call to the function, 
in addition to the extra deployment cost


**There are `2` instances of this issue:**

- [DeprecatedTransferOwnerShip.transferOwnership(address)](solidity/tmp/test_deprecated_ownable.sol#L28-L34) should be set to `payable` 

- [DeprecatedTransferOwnerShipFixed.transferOwnership(address)](solidity/tmp/test_deprecated_ownable.sol#L46-L53) should be set to `payable` 


### recommendation

Set the function to `payable`.


### locations
- solidity/tmp/test_deprecated_ownable.sol#L28-L34
- solidity/tmp/test_deprecated_ownable.sol#L46-L53

### severity
Optimization

### category
payable-function

### confidence
High

## [Optimization] Shortening revert strings to fit in 32 `bytes`

### description

In Solidity, the size of a string is not fixed and depends on the length of the string. 
Each character in a string requires 2 `bytes` of storage. 
Additionally, there is an overhead of 32 `bytes` to store the length of the string.

Shortening revert strings to fit in 32 bytes will decrease deployment time gas 
and will decrease runtime gas when the revert condition is met.


**There are `2` instances of this issue:**

- [require(bool,string)(newOwner != address(0),"Ownable: new owner is the zero address")](solidity/tmp/test_deprecated_ownable.sol#L29-L32) should be shortened strings to fit in 32 `bytes` (16 characters).

- [require(bool,string)(_pendingOwner == sender,"Ownable2Step: caller is not the new owner")](solidity/tmp/test_deprecated_ownable.sol#L62-L65) should be shortened strings to fit in 32 `bytes` (16 characters).


### recommendation

Shortening revert strings to fit in 32 `bytes`


### locations
- solidity/tmp/test_deprecated_ownable.sol#L29-L32
- solidity/tmp/test_deprecated_ownable.sol#L62-L65

### severity
Optimization

### category
revert-long-strings

### confidence
High

## [Optimization] Use `assembly` to write address storage values

### description

Where it does not affect readability, 
using assembly for simple setters allows to save gas not only on deployment, 
but also on function calls.


**There are `4` instances of this issue:**

- [oldOwner = _owner](solidity/tmp/test_deprecated_ownable.sol#L37) should use `assembly` update address to save gas.

- [_owner = newOwner](solidity/tmp/test_deprecated_ownable.sol#L38) should use `assembly` update address to save gas.

- [_pendingOwner = newOwner](solidity/tmp/test_deprecated_ownable.sol#L52) should use `assembly` update address to save gas.

- [sender = msg.sender](solidity/tmp/test_deprecated_ownable.sol#L61) should use `assembly` update address to save gas.


### recommendation

Using `assembly` update address to save gas.

For example:
```
contract Contract1 {
    address owner;

    function assemblyUpdateOwner(address newOwner) public {
        assembly {
            sstore(owner.slot, newOwner)
        }
    }
}
```


### locations
- solidity/tmp/test_deprecated_ownable.sol#L37
- solidity/tmp/test_deprecated_ownable.sol#L38
- solidity/tmp/test_deprecated_ownable.sol#L52
- solidity/tmp/test_deprecated_ownable.sol#L61

### severity
Optimization

### category
assembly-update-address

### confidence
High
