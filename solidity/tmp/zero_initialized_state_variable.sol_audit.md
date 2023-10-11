## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Missing Event Setter | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead | 3 |
| [G-1] | Remove or replace unused state variables | 3 |
| [G-2] | It costs more gas to initialize state variables to zero than to let the default of zero be applied | 3 |
| [G-3] | Use `delete` to Clear Variables | 3 |
| [G-4] | State variables that could be declared constant | 9 |



## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There is `1` instance of this issue:**

- Setter function [SetVsDefault1.slitherConstructorVariables()](solidity/tmp/zero_initialized_state_variable.sol#L1-L11) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/zero_initialized_state_variable.sol#L1-L11

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

## [Optimization] Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead

### description

> When using elements that are smaller than 32 bytes, your contract’s gas usage may be higher. This is because the EVM operates on 32 bytes at a time. Therefore, if the element is smaller than that, the EVM must use more operations in order to reduce the size of the element from 32 bytes to the desired size.

More detail see [this.](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html)

Each operation involving a `uint8` costs an extra [**22-28 gas**](https://gist.github.com/0xxfu/3672fec07eb3031cd5da14ac015e04a1) (depending on whether the other operand is also a variable of type `uint8`) as compared to ones involving `uint256`, due to the compiler having to clear the higher bits of the memory word before operating on the `uint8`, as well as the associated stack operations of doing so. Use a larger size then downcast where needed


**There are `3` instances of this issue:**

- `uint32 `[SetVsDefault1.bad2](solidity/tmp/zero_initialized_state_variable.sol#L3) should be used `uint256/int256`.

- `uint32 `[SetVsDefault1.notBad2](solidity/tmp/zero_initialized_state_variable.sol#L5) should be used `uint256/int256`.

- `uint32 `[SetVsDefault1.good2](solidity/tmp/zero_initialized_state_variable.sol#L9) should be used `uint256/int256`.


### recommendation

Using `uint256/int256` replace `uint128/uint64/uint32/uint16/uint8` or `int128/int64/int32/int16/int8`


### locations
- solidity/tmp/zero_initialized_state_variable.sol#L3
- solidity/tmp/zero_initialized_state_variable.sol#L5
- solidity/tmp/zero_initialized_state_variable.sol#L9

### severity
Optimization

### category
smaller-uint-int

### confidence
High

## [Optimization] Remove or replace unused state variables

### description

Saves a storage slot. If the variable is assigned a non-zero value, 
saves Gsset (20000 gas). If it's assigned a zero value, saves Gsreset (2900 gas). 
If the variable remains unassigned, there is no gas savings unless the variable is public, 
in which case the compiler-generated non-payable getter deployment cost is saved. 
If the state variable is overriding an interface's public function, 
mark the variable as constant or immutable so that it does not use a storage slot


**There are `3` instances of this issue:**

- [SetVsDefault1.good](solidity/tmp/zero_initialized_state_variable.sol#L8) is never used.
- [SetVsDefault1.good2](solidity/tmp/zero_initialized_state_variable.sol#L9) is never used.
- [SetVsDefault1.good3](solidity/tmp/zero_initialized_state_variable.sol#L10) is never used.

### recommendation

Remove or replace the unused state variables


### locations
- solidity/tmp/zero_initialized_state_variable.sol#L8
- solidity/tmp/zero_initialized_state_variable.sol#L9
- solidity/tmp/zero_initialized_state_variable.sol#L10

### severity
Optimization

### category
unused-state-variables

### confidence
High

## [Optimization] It costs more gas to initialize state variables to zero than to let the default of zero be applied

### description

If a state variable is not set/initialized, 
it is assumed to have the default value (0 for uint, false for bool, address(0) for address…). 
Explicitly initializing it with its default value is an anti-pattern and wastes gas.

More detail see [this.](https://gist.github.com/0xxfu/b111e822aa4ee2e0f6bbaf2658818520)



**There are `3` instances of this issue:**

- [SetVsDefault1.bad](solidity/tmp/zero_initialized_state_variable.sol#L2) should not overwrite the default.

- [SetVsDefault1.bad2](solidity/tmp/zero_initialized_state_variable.sol#L3) should not overwrite the default.

- [SetVsDefault1.bad3](solidity/tmp/zero_initialized_state_variable.sol#L6) should not overwrite the default.


### recommendation

Do not initialize state variables to zero.


### locations
- solidity/tmp/zero_initialized_state_variable.sol#L2
- solidity/tmp/zero_initialized_state_variable.sol#L3
- solidity/tmp/zero_initialized_state_variable.sol#L6

### severity
Optimization

### category
zero-initialized-state-variable

### confidence
High

## [Optimization] Use `delete` to Clear Variables

### description

delete a assigns the initial value for the type to a. i.e. 
for integers it is equivalent to a = 0, but it can also be used on arrays, 
where it assigns a dynamic array of length zero or a static array of the same 
length with all elements reset. For structs, it assigns a struct with all members reset. 
Similarly, it can also be used to set an address to zero address. 
It has no effect on whole mappings though (as the keys of mappings may be arbitrary 
and are generally unknown). However, individual keys and what they map to can be deleted: 
If a is a mapping, then delete a[x] will delete the value stored at x.

The delete key better conveys the intention and is also more idiomatic. 
Consider replacing assignments of zero with delete statements.


**There are `3` instances of this issue:**

- Should use `delete` statement instead of [bad = 0](solidity/tmp/zero_initialized_state_variable.sol#L2)

- Should use `delete` statement instead of [bad2 = 0](solidity/tmp/zero_initialized_state_variable.sol#L3)

- Should use `delete` statement instead of [bad3 = address(0)](solidity/tmp/zero_initialized_state_variable.sol#L6)


### recommendation

Replacing assignments of zero with delete statements.



### locations
- solidity/tmp/zero_initialized_state_variable.sol#L2
- solidity/tmp/zero_initialized_state_variable.sol#L3
- solidity/tmp/zero_initialized_state_variable.sol#L6

### severity
Optimization

### category
use-delete-statement

### confidence
High

## [Optimization] State variables that could be declared constant

### description
Constant state variables should be declared constant to save gas.

**There are `9` instances of this issue:**

- [SetVsDefault1.bad](solidity/tmp/zero_initialized_state_variable.sol#L2) should be constant

- [SetVsDefault1.bad2](solidity/tmp/zero_initialized_state_variable.sol#L3) should be constant

- [SetVsDefault1.notBad](solidity/tmp/zero_initialized_state_variable.sol#L4) should be constant

- [SetVsDefault1.notBad2](solidity/tmp/zero_initialized_state_variable.sol#L5) should be constant

- [SetVsDefault1.bad3](solidity/tmp/zero_initialized_state_variable.sol#L6) should be constant

- [SetVsDefault1.notBad3](solidity/tmp/zero_initialized_state_variable.sol#L7) should be constant

- [SetVsDefault1.good](solidity/tmp/zero_initialized_state_variable.sol#L8) should be constant

- [SetVsDefault1.good2](solidity/tmp/zero_initialized_state_variable.sol#L9) should be constant

- [SetVsDefault1.good3](solidity/tmp/zero_initialized_state_variable.sol#L10) should be constant


### recommendation
Add the `constant` attributes to state variables that never change.

### locations
- solidity/tmp/zero_initialized_state_variable.sol#L2
- solidity/tmp/zero_initialized_state_variable.sol#L3
- solidity/tmp/zero_initialized_state_variable.sol#L4
- solidity/tmp/zero_initialized_state_variable.sol#L5
- solidity/tmp/zero_initialized_state_variable.sol#L6
- solidity/tmp/zero_initialized_state_variable.sol#L7
- solidity/tmp/zero_initialized_state_variable.sol#L8
- solidity/tmp/zero_initialized_state_variable.sol#L9
- solidity/tmp/zero_initialized_state_variable.sol#L10

### severity
Optimization

### category
state-should-be-constant

### confidence
High
