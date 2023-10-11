## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Setters should check the input value | 2 |
| [L-1] | Unsafe to use floating pragma | 1 |
| [L-2] | Missing Event Setter | 6 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 2 |
| [N-1] | Conformance to Solidity naming conventions | 3 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Use `uint256(1)/uint256(2)` instead for `true` and `false` boolean states | 1 |
| [G-1] | Should use latest solidity version `0.8.21` for gas reduction and improved security. | 1 |
| [G-2] | Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead | 3 |



## [Low] Setters should check the input value

### description

Setters should have initial value check to prevent assigning wrong value to the variable. 
Assignment of wrong value can lead to unexpected behavior of the contract.


**There are `2` instances of this issue:**

- [MappingUint8s.set2(uint8).value](solidity/tmp/test_bool_state_variables.sol#L38) lacks an upper limit check on :
	- [data2 = value](solidity/tmp/test_bool_state_variables.sol#L39)

- [MappingUint256s.set2(uint256).value](solidity/tmp/test_bool_state_variables.sol#L55) lacks an upper limit check on :
	- [data2 = value](solidity/tmp/test_bool_state_variables.sol#L56)


### recommendation

Add an upper limit check to the setters function.


### locations
- solidity/tmp/test_bool_state_variables.sol#L38
- solidity/tmp/test_bool_state_variables.sol#L55

### severity
Low

### category
unchecked-setters

### confidence
High

## [Low] Unsafe to use floating pragma

### description

Contracts should be deployed with the same compiler version and flags that 
they have been tested with thoroughly. 
Locking the pragma helps to ensure that contracts do not accidentally get deployed using, 
for example, an outdated compiler version that might introduce bugs that affect the 
contract system negatively.

More detail see [SWC-103](https://swcregistry.io/docs/SWC-103).


**There is `1` instance of this issue:**

- Should lock the pragma version instead of floating pragma: [^0.8.17](solidity/tmp/test_bool_state_variables.sol#L2). 


### recommendation

Lock the pragma version and also consider known bugs (https://github.com/ethereum/solidity/releases) 
for the compiler version that is chosen.


### locations
- solidity/tmp/test_bool_state_variables.sol#L2

### severity
Low

### category
unsafe-floating-pragma

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `6` instances of this issue:**

- Setter function [MappingBools.set_a81(uint256,bool)](solidity/tmp/test_bool_state_variables.sol#L15-L17) does not emit an event

- Setter function [MappingBools.set2(bool)](solidity/tmp/test_bool_state_variables.sol#L21-L23) does not emit an event

- Setter function [MappingUint8s.set_Hl1r(uint256,uint8)](solidity/tmp/test_bool_state_variables.sol#L32-L34) does not emit an event

- Setter function [MappingUint8s.set2(uint8)](solidity/tmp/test_bool_state_variables.sol#L38-L40) does not emit an event

- Setter function [MappingUint256s.set_2E3(uint256,uint256)](solidity/tmp/test_bool_state_variables.sol#L49-L51) does not emit an event

- Setter function [MappingUint256s.set2(uint256)](solidity/tmp/test_bool_state_variables.sol#L55-L57) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/test_bool_state_variables.sol#L15-L17
- solidity/tmp/test_bool_state_variables.sol#L21-L23
- solidity/tmp/test_bool_state_variables.sol#L32-L34
- solidity/tmp/test_bool_state_variables.sol#L38-L40
- solidity/tmp/test_bool_state_variables.sol#L49-L51
- solidity/tmp/test_bool_state_variables.sol#L55-L57

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

**There are `2` instances of this issue:**

- Pragma version[^0.8.17](solidity/tmp/test_bool_state_variables.sol#L2) allows old versions

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
- solidity/tmp/test_bool_state_variables.sol#L2
- 

### severity
Informational

### category
solc-version

### confidence
High

## [Informational] Conformance to Solidity naming conventions

### description

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There are `3` instances of this issue:**

- Function [MappingBools.set_a81(uint256,bool)](solidity/tmp/test_bool_state_variables.sol#L15-L17) is not in mixedCase

- Function [MappingUint8s.set_Hl1r(uint256,uint8)](solidity/tmp/test_bool_state_variables.sol#L32-L34) is not in mixedCase

- Function [MappingUint256s.set_2E3(uint256,uint256)](solidity/tmp/test_bool_state_variables.sol#L49-L51) is not in mixedCase


### recommendation
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations
- solidity/tmp/test_bool_state_variables.sol#L15-L17
- solidity/tmp/test_bool_state_variables.sol#L32-L34
- solidity/tmp/test_bool_state_variables.sol#L49-L51

### severity
Informational

### category
naming-convention

### confidence
High

## [Optimization] Use `uint256(1)/uint256(2)` instead for `true` and `false` boolean states

### description

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
    


**There is `1` instance of this issue:**

- bool state [MappingBools.data2](solidity/tmp/test_bool_state_variables.sol#L11) should be replaced by `uint256(1)` and `uint256(2)`

### recommendation
Use `uint256(1)` and `uint256(2)` for true/false to avoid a Gwarmaccess (**[100 gas](https://gist.github.com/0xxfu/d12e22af63cd2e0e9d6a8550360b2959)**) for the extra SLOAD, and to avoid Gsset (**20000 gas**) when changing from `false` to `true`, after having been `true` in the past

### locations
- solidity/tmp/test_bool_state_variables.sol#L11

### severity
Optimization

### category
bool-state-variables

### confidence
High

## [Optimization] Should use latest solidity version `0.8.21` for gas reduction and improved security.

### description

[Solidity `0.8.21`](https://soliditylang.org/blog/2023/07/19/solidity-0.8.21-release-announcement) has many optimization with compiler and bugfixes, 
please upgrade Solidity to the latest version(`0.8.21`) for gas reduction and improved security.


**There is `1` instance of this issue:**

- pragma solidity version [^0.8.17](solidity/tmp/test_bool_state_variables.sol#L2) should upgrade to the latest version: 0.8.21

### recommendation
Upgrade solidity version to the latest version: 0.8.21

### locations
- solidity/tmp/test_bool_state_variables.sol#L2

### severity
Optimization

### category
upgrade-to-latest

### confidence
High

## [Optimization] Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead

### description

> When using elements that are smaller than 32 bytes, your contract’s gas usage may be higher. This is because the EVM operates on 32 bytes at a time. Therefore, if the element is smaller than that, the EVM must use more operations in order to reduce the size of the element from 32 bytes to the desired size.

More detail see [this.](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html)

Each operation involving a `uint8` costs an extra [**22-28 gas**](https://gist.github.com/0xxfu/3672fec07eb3031cd5da14ac015e04a1) (depending on whether the other operand is also a variable of type `uint8`) as compared to ones involving `uint256`, due to the compiler having to clear the higher bits of the memory word before operating on the `uint8`, as well as the associated stack operations of doing so. Use a larger size then downcast where needed


**There are `3` instances of this issue:**

- `uint8 `[MappingUint8s.data2](solidity/tmp/test_bool_state_variables.sol#L28) should be used `uint256/int256`.

- `uint8 `[MappingUint8s.set_Hl1r(uint256,uint8).value](solidity/tmp/test_bool_state_variables.sol#L32) should be used `uint256/int256`.

- `uint8 `[MappingUint8s.set2(uint8).value](solidity/tmp/test_bool_state_variables.sol#L38) should be used `uint256/int256`.


### recommendation

Using `uint256/int256` replace `uint128/uint64/uint32/uint16/uint8` or `int128/int64/int32/int16/int8`


### locations
- solidity/tmp/test_bool_state_variables.sol#L28
- solidity/tmp/test_bool_state_variables.sol#L32
- solidity/tmp/test_bool_state_variables.sol#L38

### severity
Optimization

### category
smaller-uint-int

### confidence
High
