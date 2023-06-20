## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Missing events access control | 3 |
| [L-1] | Missing zero address validation | 2 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | `<x> += <y>` costs more gas than `<x> = <x> + <y>` for state variables | 1 |
| [G-1] | Dead-code: functions not used should be removed to save deployment gas | 1 |
| [G-2] | Use indexed events for value types as they are less costly compared to non-indexed ones | 2 |
| [G-3] | use custom errors instead of revert strings | 1 |
| [G-4] | State variables that could be declared constant | 1 |



## [Low] Missing events access control

### description:
Detect missing events for critical access control parameters

**There are `3` instances of this issue:**

- [Bug.bad0()](solidity/missing_zero_address_validation.sol#L15-L17) should emit an event for: 
	- [owner = msg.sender](solidity/missing_zero_address_validation.sol#L16) 

- [Bug.bad1(address)](solidity/missing_zero_address_validation.sol#L19-L21) should emit an event for: 
	- [owner = newOwner](solidity/missing_zero_address_validation.sol#L20) 

- [Bug.bad2(address)](solidity/missing_zero_address_validation.sol#L23-L26) should emit an event for: 
	- [owner = newOwner](solidity/missing_zero_address_validation.sol#L25) 

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
`updateOwner()` has no event, so it is difficult to track off-chain owner changes.


### recommendation:
Emit an event for critical parameter changes.

### locations:
- solidity/missing_zero_address_validation.sol#L15-L17
- solidity/missing_zero_address_validation.sol#L19-L21
- solidity/missing_zero_address_validation.sol#L23-L26

### severity:
Low

### category:
events-access

## [Low] Missing zero address validation

### description:
Detect missing zero address validation.

**There are `2` instances of this issue:**

- [Bug.good5(address).newOwner](solidity/missing_zero_address_validation.sol#L49) lacks a zero-check on :
		- [operator = newOwner](solidity/missing_zero_address_validation.sol#L50)

- [Bug.bad1(address).newOwner](solidity/missing_zero_address_validation.sol#L19) lacks a zero-check on :
		- [owner = newOwner](solidity/missing_zero_address_validation.sol#L20)

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
- solidity/missing_zero_address_validation.sol#L49
- solidity/missing_zero_address_validation.sol#L19

### severity:
Low

### category:
missing-zero-check

## [Optimization] `<x> += <y>` costs more gas than `<x> = <x> + <y>` for state variables

### description:
Using the addition operator instead of plus-equals saves **[113 gas](https://gist.github.com/0xxfu/86ae4bdd07d7db169cea110dba5a5af4)**

**There is `1` instance of this issue:**

- should use arithmetic operator `=` replace `+=` in [totalSupply += a](solidity/missing_zero_address_validation.sol#L29)

### recommendation:
Using arithmetic operator `=` replace assignment operator `+=` or `-=` 

### locations:
- solidity/missing_zero_address_validation.sol#L29

### severity:
Optimization

### category:
assignment-left-operation

## [Optimization] Dead-code: functions not used should be removed to save deployment gas

### description:
Functions that are not sued.

**There is `1` instance of this issue:**

- [Bug.good3(address)](solidity/missing_zero_address_validation.sol#L41-L43) is never used and should be removed


### recommendation:
Remove unused functions.

### locations:
- solidity/missing_zero_address_validation.sol#L41-L43

### severity:
Optimization

### category:
dead-code

## [Optimization] Use indexed events for value types as they are less costly compared to non-indexed ones

### description:

Using the `indexed` keyword for [value types](https://docs.soliditylang.org/en/v0.8.20/types.html#value-types) (`bool/int/address/string/bytes`) saves gas costs, as seen in [this example](https://gist.github.com/0xxfu/c292a65ecb61cae6fd2090366ea0877e).

However, this is only the case for value types, whereas indexing [reference types](https://docs.soliditylang.org/en/v0.8.20/types.html#reference-types) (`array/struct`) are more expensive than their unindexed version.


**There are `2` instances of this issue:**

- The following variables should be indexed in [Bug.Owner(address)](solidity/missing_zero_address_validation.sol#L8):

	- [owner](solidity/missing_zero_address_validation.sol#L8)

- The following variables should be indexed in [Bug.Supply(uint256)](solidity/missing_zero_address_validation.sol#L7):

	- [totalSupply](solidity/missing_zero_address_validation.sol#L7)


### recommendation:

Using the `indexed` keyword for values types `bool/int/address/string/bytes` in event


### locations:
- solidity/missing_zero_address_validation.sol#L8
- solidity/missing_zero_address_validation.sol#L7

### severity:
Optimization

### category:
unindexed-event

## [Optimization] use custom errors instead of revert strings

### description:

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There is `1` instance of this issue:**

- [require(bool)(newOwner != address(0))](solidity/missing_zero_address_validation.sol#L24) should use custom error to save gas.


### recommendation:

Using custom errors replace `require` or `assert`.


### locations:
- solidity/missing_zero_address_validation.sol#L24

### severity:
Optimization

### category:
use-custom-error

## [Optimization] State variables that could be declared constant

### description:
State variables that are not updated following deployment should be declared constant to save gas.

**There is `1` instance of this issue:**

- [Bug.addr](solidity/missing_zero_address_validation.sol#L6) should be constant 


### recommendation:
Add the `constant` attribute to state variables that never change.

### locations:
- solidity/missing_zero_address_validation.sol#L6

### severity:
Optimization

### category:
constable-states
