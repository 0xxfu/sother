## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Unsafe downcasting arithmetic operation | 7 |
| [L-1] | Double type casts create complexity within the code | 4 |
| [L-2] | Setters should check the input value | 6 |
| [L-3] | Events are missing sender information | 1 |
| [L-4] | Missing Event Setter | 5 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Unnecessary Public Function Modifier | 2 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead | 13 |
| [G-1] | Remove or replace unused state variables | 3 |
| [G-2] | Dead-code: functions not used should be removed to save deployment gas | 4 |
| [G-3] | Use indexed events for value types as they are less costly compared to non-indexed ones | 1 |
| [G-4] | State variables that could be declared constant | 3 |
| [G-5] | State variables that could be declared constant | 3 |



## [Low] Unsafe downcasting arithmetic operation

### description

Downcasting from uint256/int256 in Solidity does not revert on overflow.
When a type is downcast to a smaller type, the higher order bits are truncated, 
effectively applying a modulo to the original value. 
Without any other checks, this wrapping will lead to unexpected behavior and bugs.


**There are `7` instances of this issue:**

- [ui128 = uint128(a)](solidity/tmp/unsafe_casting.sol#L16) should use `uint256/int256` or `OpenZeppelin SafeCast lib`.
- [ui32 = uint32(block.timestamp)](solidity/tmp/unsafe_casting.sol#L18) should use `uint256/int256` or `OpenZeppelin SafeCast lib`.
- [Transmitted(uint32(uint256(a >> 8)))](solidity/tmp/unsafe_casting.sol#L20) should use `uint256/int256` or `OpenZeppelin SafeCast lib`.
- [uint32(a)](solidity/tmp/unsafe_casting.sol#L24) should use `uint256/int256` or `OpenZeppelin SafeCast lib`.
- [ui128 = uint128(uint64(a))](solidity/tmp/unsafe_casting.sol#L78) should use `uint256/int256` or `OpenZeppelin SafeCast lib`.
- [ui32 = uint32(uint64(block.timestamp))](solidity/tmp/unsafe_casting.sol#L80) should use `uint256/int256` or `OpenZeppelin SafeCast lib`.
- [uint32(uint8(a))](solidity/tmp/unsafe_casting.sol#L84) should use `uint256/int256` or `OpenZeppelin SafeCast lib`.

### recommendation

Just use `uint256/int256`, or use [OpenZeppelin SafeCast lib](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/math/SafeCast.sol#).


### locations
- solidity/tmp/unsafe_casting.sol#L16
- solidity/tmp/unsafe_casting.sol#L18
- solidity/tmp/unsafe_casting.sol#L20
- solidity/tmp/unsafe_casting.sol#L24
- solidity/tmp/unsafe_casting.sol#L78
- solidity/tmp/unsafe_casting.sol#L80
- solidity/tmp/unsafe_casting.sol#L84

### severity
Low

### category
unsafe-downcast

### confidence
High

## [Low] Double type casts create complexity within the code

### description

Double type casting should be avoided in Solidity contracts to prevent unintended 
consequences and ensure accurate data representation. 
Performing multiple type casts in succession can lead to unexpected truncation, 
rounding errors, or loss of precision, potentially compromising the contract's 
functionality and reliability. Furthermore, double type casting can make the code 
less readable and harder to maintain, increasing the likelihood of errors and 
misunderstandings during development and debugging. To ensure precise and consistent 
data handling, developers should use appropriate data types and avoid unnecessary 
or excessive type casting, promoting a more robust and dependable contract execution.


**There are `4` instances of this issue:**

- [Transmitted(uint32(uint256(a >> 8)))](solidity/tmp/unsafe_casting.sol#L20) should use single casting instead of double casting.

- [ui128 = uint128(uint64(a))](solidity/tmp/unsafe_casting.sol#L78) should use single casting instead of double casting.

- [ui32 = uint32(uint64(block.timestamp))](solidity/tmp/unsafe_casting.sol#L80) should use single casting instead of double casting.

- [uint32(uint8(a))](solidity/tmp/unsafe_casting.sol#L84) should use single casting instead of double casting.


### recommendation

Consider using single casting instead of double casting.


### locations
- solidity/tmp/unsafe_casting.sol#L20
- solidity/tmp/unsafe_casting.sol#L78
- solidity/tmp/unsafe_casting.sol#L80
- solidity/tmp/unsafe_casting.sol#L84

### severity
Low

### category
unsafe-double-cast

### confidence
High

## [Low] Setters should check the input value

### description

Setters should have initial value check to prevent assigning wrong value to the variable. 
Assignment of wrong value can lead to unexpected behavior of the contract.


**There are `6` instances of this issue:**

- [UnsafeDowncast.bad(uint256).a](solidity/tmp/unsafe_casting.sol#L15) lacks an upper limit check on :
	- [ui128 = uint128(a)](solidity/tmp/unsafe_casting.sol#L16)

- [UnsafeDowncast.notBad(uint256).a](solidity/tmp/unsafe_casting.sol#L27) lacks an upper limit check on :
	- [ui128 = toUint128(a)](solidity/tmp/unsafe_casting.sol#L28)

- [UnsafeDowncast.notBad2(uint256).a](solidity/tmp/unsafe_casting.sol#L31) lacks an upper limit check on :
	- [i256 = int256(a)](solidity/tmp/unsafe_casting.sol#L32)

- [UnsafeDoubleCast.bad(uint256).a](solidity/tmp/unsafe_casting.sol#L77) lacks an upper limit check on :
	- [ui128 = uint128(uint64(a))](solidity/tmp/unsafe_casting.sol#L78)

- [UnsafeDoubleCast.notBad(uint256).a](solidity/tmp/unsafe_casting.sol#L87) lacks an upper limit check on :
	- [ui128 = toUint128(a)](solidity/tmp/unsafe_casting.sol#L88)

- [UnsafeDoubleCast.notBad2(uint256).a](solidity/tmp/unsafe_casting.sol#L91) lacks an upper limit check on :
	- [i256 = int256(a)](solidity/tmp/unsafe_casting.sol#L92)


### recommendation

Add an upper limit check to the setters function.


### locations
- solidity/tmp/unsafe_casting.sol#L15
- solidity/tmp/unsafe_casting.sol#L27
- solidity/tmp/unsafe_casting.sol#L31
- solidity/tmp/unsafe_casting.sol#L77
- solidity/tmp/unsafe_casting.sol#L87
- solidity/tmp/unsafe_casting.sol#L91

### severity
Low

### category
unchecked-setters

### confidence
High

## [Low] Events are missing sender information

### description

When an action is triggered based on a user's action, not being able to filter based on 
who triggered the action makes event processing a lot more cumbersome. 
Including the `msg.sender` the events of these types of action will make events much more 
useful to end users.



**There is `1` instance of this issue:**

- [Transmitted(uint32(uint256(a >> 8)))](solidity/tmp/unsafe_casting.sol#L20) should add `msg.sender` to event.


### recommendation

Adding `msg.sender` to event.


### locations
- solidity/tmp/unsafe_casting.sol#L20

### severity
Low

### category
missing-sender-in-event

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `5` instances of this issue:**

- Setter function [UnsafeDowncast.notBad(uint256)](solidity/tmp/unsafe_casting.sol#L27-L29) does not emit an event

- Setter function [UnsafeDowncast.notBad2(uint256)](solidity/tmp/unsafe_casting.sol#L31-L33) does not emit an event

- Setter function [UnsafeDoubleCast.bad(uint256)](solidity/tmp/unsafe_casting.sol#L77-L81) does not emit an event

- Setter function [UnsafeDoubleCast.notBad(uint256)](solidity/tmp/unsafe_casting.sol#L87-L89) does not emit an event

- Setter function [UnsafeDoubleCast.notBad2(uint256)](solidity/tmp/unsafe_casting.sol#L91-L93) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/unsafe_casting.sol#L27-L29
- solidity/tmp/unsafe_casting.sol#L31-L33
- solidity/tmp/unsafe_casting.sol#L77-L81
- solidity/tmp/unsafe_casting.sol#L87-L89
- solidity/tmp/unsafe_casting.sol#L91-L93

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

- function:[UnsafeDowncast.bad2(uint128)](solidity/tmp/unsafe_casting.sol#L23-L25)is public and can be replaced with external 

- function:[UnsafeDoubleCast.bad2(uint128)](solidity/tmp/unsafe_casting.sol#L83-L85)is public and can be replaced with external 

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
- solidity/tmp/unsafe_casting.sol#L23-L25
- solidity/tmp/unsafe_casting.sol#L83-L85

### severity
Informational

### category
unnecessary-public-function-modifier

### confidence
High

## [Optimization] Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead

### description

> When using elements that are smaller than 32 bytes, your contract’s gas usage may be higher. This is because the EVM operates on 32 bytes at a time. Therefore, if the element is smaller than that, the EVM must use more operations in order to reduce the size of the element from 32 bytes to the desired size.

More detail see [this.](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html)

Each operation involving a `uint8` costs an extra [**22-28 gas**](https://gist.github.com/0xxfu/3672fec07eb3031cd5da14ac015e04a1) (depending on whether the other operand is also a variable of type `uint8`) as compared to ones involving `uint256`, due to the compiler having to clear the higher bits of the memory word before operating on the `uint8`, as well as the associated stack operations of doing so. Use a larger size then downcast where needed


**There are `13` instances of this issue:**

- `uint128 `[UnsafeDowncast.ui128](solidity/tmp/unsafe_casting.sol#L3) should be used `uint256/int256`.

- `uint32 `[UnsafeDowncast.ui32](solidity/tmp/unsafe_casting.sol#L4) should be used `uint256/int256`.

- `int8 `[UnsafeDowncast.i8](solidity/tmp/unsafe_casting.sol#L7) should be used `uint256/int256`.

- `uint32 `[UnsafeDowncast.bad2(uint128).](solidity/tmp/unsafe_casting.sol#L23) should be used `uint256/int256`.

- `uint128 `[UnsafeDowncast.bad2(uint128).a](solidity/tmp/unsafe_casting.sol#L23) should be used `uint256/int256`.

- `uint128 `[UnsafeDowncast.toUint128(uint256).](solidity/tmp/unsafe_casting.sol#L35) should be used `uint256/int256`.

- `uint8 `[UnsafeDowncast.toUint8(uint256).](solidity/tmp/unsafe_casting.sol#L42) should be used `uint256/int256`.

- `int8 `[UnsafeDowncast.toInt8(int256).downcasted](solidity/tmp/unsafe_casting.sol#L56) should be used `uint256/int256`.

- `uint128 `[UnsafeDoubleCast.ui128](solidity/tmp/unsafe_casting.sol#L73) should be used `uint256/int256`.

- `uint32 `[UnsafeDoubleCast.ui32](solidity/tmp/unsafe_casting.sol#L74) should be used `uint256/int256`.

- `uint32 `[UnsafeDoubleCast.bad2(uint128).](solidity/tmp/unsafe_casting.sol#L83) should be used `uint256/int256`.

- `uint128 `[UnsafeDoubleCast.bad2(uint128).a](solidity/tmp/unsafe_casting.sol#L83) should be used `uint256/int256`.

- `uint128 `[UnsafeDoubleCast.toUint128(uint256).](solidity/tmp/unsafe_casting.sol#L95) should be used `uint256/int256`.


### recommendation

Using `uint256/int256` replace `uint128/uint64/uint32/uint16/uint8` or `int128/int64/int32/int16/int8`


### locations
- solidity/tmp/unsafe_casting.sol#L3
- solidity/tmp/unsafe_casting.sol#L4
- solidity/tmp/unsafe_casting.sol#L7
- solidity/tmp/unsafe_casting.sol#L23
- solidity/tmp/unsafe_casting.sol#L23
- solidity/tmp/unsafe_casting.sol#L35
- solidity/tmp/unsafe_casting.sol#L42
- solidity/tmp/unsafe_casting.sol#L56
- solidity/tmp/unsafe_casting.sol#L73
- solidity/tmp/unsafe_casting.sol#L74
- solidity/tmp/unsafe_casting.sol#L83
- solidity/tmp/unsafe_casting.sol#L83
- solidity/tmp/unsafe_casting.sol#L95

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

- [UnsafeDowncast.ui256](solidity/tmp/unsafe_casting.sol#L2) is never used.
- [UnsafeDowncast.i8](solidity/tmp/unsafe_casting.sol#L7) is never used.
- [UnsafeDoubleCast.ui256](solidity/tmp/unsafe_casting.sol#L72) is never used.

### recommendation

Remove or replace the unused state variables


### locations
- solidity/tmp/unsafe_casting.sol#L2
- solidity/tmp/unsafe_casting.sol#L7
- solidity/tmp/unsafe_casting.sol#L72

### severity
Optimization

### category
unused-state-variables

### confidence
High

## [Optimization] Dead-code: functions not used should be removed to save deployment gas

### description
Functions that are not sued.

**There are `4` instances of this issue:**

- [UnsafeDowncast.toUint8(uint256)](solidity/tmp/unsafe_casting.sol#L42-L47) is never used and should be removed

- [UnsafeDowncast.toUint256(int256)](solidity/tmp/unsafe_casting.sol#L49-L54) is never used and should be removed

- [UnsafeDowncast.toInt8(int256)](solidity/tmp/unsafe_casting.sol#L56-L61) is never used and should be removed

- [UnsafeDowncast.toInt256(uint256)](solidity/tmp/unsafe_casting.sol#L63-L68) is never used and should be removed


### recommendation
Remove unused functions.

### locations
- solidity/tmp/unsafe_casting.sol#L42-L47
- solidity/tmp/unsafe_casting.sol#L49-L54
- solidity/tmp/unsafe_casting.sol#L56-L61
- solidity/tmp/unsafe_casting.sol#L63-L68

### severity
Optimization

### category
dead-code

### confidence
High

## [Optimization] Use indexed events for value types as they are less costly compared to non-indexed ones

### description

Using the `indexed` keyword for [value types](https://docs.soliditylang.org/en/v0.8.20/types.html#value-types) (`bool/int/address/string/bytes`) saves gas costs, as seen in [this example](https://gist.github.com/0xxfu/c292a65ecb61cae6fd2090366ea0877e).

However, this is only the case for value types, whereas indexing [reference types](https://docs.soliditylang.org/en/v0.8.20/types.html#reference-types) (`array/struct`) are more expensive than their unindexed version.


**There is `1` instance of this issue:**

- The following variables should be indexed in [UnsafeDowncast.Transmitted(uint32)](solidity/tmp/unsafe_casting.sol#L8):

	- [ue](solidity/tmp/unsafe_casting.sol#L8)


### recommendation

Using the `indexed` keyword for values types `bool/int/address/string/bytes` in event


### locations
- solidity/tmp/unsafe_casting.sol#L8

### severity
Optimization

### category
unindexed-event

### confidence
High

## [Optimization] State variables that could be declared constant

### description
State variables that are not updated following deployment should be declared constant to save gas.

**There are `3` instances of this issue:**

- [UnsafeDowncast.ui256](solidity/tmp/unsafe_casting.sol#L2) should be constant 

- [UnsafeDowncast.i8](solidity/tmp/unsafe_casting.sol#L7) should be constant 

- [UnsafeDoubleCast.ui256](solidity/tmp/unsafe_casting.sol#L72) should be constant 


### recommendation
Add the `constant` attribute to state variables that never change.

### locations
- solidity/tmp/unsafe_casting.sol#L2
- solidity/tmp/unsafe_casting.sol#L7
- solidity/tmp/unsafe_casting.sol#L72

### severity
Optimization

### category
constable-states

### confidence
High

## [Optimization] State variables that could be declared constant

### description
Constant state variables should be declared constant to save gas.

**There are `3` instances of this issue:**

- [UnsafeDowncast.ui256](solidity/tmp/unsafe_casting.sol#L2) should be constant

- [UnsafeDowncast.i8](solidity/tmp/unsafe_casting.sol#L7) should be constant

- [UnsafeDoubleCast.ui256](solidity/tmp/unsafe_casting.sol#L72) should be constant


### recommendation
Add the `constant` attributes to state variables that never change.

### locations
- solidity/tmp/unsafe_casting.sol#L2
- solidity/tmp/unsafe_casting.sol#L7
- solidity/tmp/unsafe_casting.sol#L72

### severity
Optimization

### category
state-should-be-constant

### confidence
High
