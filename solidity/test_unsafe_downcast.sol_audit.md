## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Unsafe downcasting arithmetic operation | 4 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Unused state variable | 2 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Dead-code: functions not used should be removed to save deployment gas | 4 |
| [G-1] | `internal` functions only called once can be inlined to save gas | 1 |
| [G-2] | Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead | 8 |
| [G-3] | Use indexed events for value types as they are less costly compared to non-indexed ones | 1 |
| [G-4] | Remove or replace unused state variables | 2 |
| [G-5] | State variables that could be declared constant | 2 |



## [Low] Unsafe downcasting arithmetic operation

### description:

Downcasting from uint256/int256 in Solidity does not revert on overflow.
When a type is downcast to a smaller type, the higher order bits are truncated, 
effectively applying a modulo to the original value. 
Without any other checks, this wrapping will lead to unexpected behavior and bugs.


**There are `4` instances of this issue:**

- `ui128 = uint128(a)` (solidity/test_unsafe_downcast.sol#L16) should use `uint256/int256` or `OpenZeppelin SafeCast lib`.
- `ui32 = uint32(block.timestamp)` (solidity/test_unsafe_downcast.sol#L18) should use `uint256/int256` or `OpenZeppelin SafeCast lib`.
- `Transmitted(uint32(uint256(a >> 8)))` (solidity/test_unsafe_downcast.sol#L20) should use `uint256/int256` or `OpenZeppelin SafeCast lib`.
- `uint32(a)` (solidity/test_unsafe_downcast.sol#L24) should use `uint256/int256` or `OpenZeppelin SafeCast lib`.

### recommendation:

Just use `uint256/int256`, or use [OpenZeppelin SafeCast lib](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/math/SafeCast.sol#).


### locations:
- solidity/test_unsafe_downcast.sol#L16
- solidity/test_unsafe_downcast.sol#L18
- solidity/test_unsafe_downcast.sol#L20
- solidity/test_unsafe_downcast.sol#L24

### severity:
Low

### category:
unsafe-downcast

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

## [Informational] Unused state variable

### description:
Unused state variable.

**There are `2` instances of this issue:**

- `UnsafeDowncast.ui256` (solidity/test_unsafe_downcast.sol#L2) is never used in `UnsafeDowncast` (solidity/test_unsafe_downcast.sol#L1-L69)

- `UnsafeDowncast.i8` (solidity/test_unsafe_downcast.sol#L7) is never used in `UnsafeDowncast` (solidity/test_unsafe_downcast.sol#L1-L69)


### recommendation:
Remove unused state variables.

### locations:
- solidity/test_unsafe_downcast.sol#L2
- solidity/test_unsafe_downcast.sol#L7

### severity:
Informational

### category:
unused-state

## [Optimization] Dead-code: functions not used should be removed to save deployment gas

### description:
Functions that are not sued.

**There are `4` instances of this issue:**

- `UnsafeDowncast.toUint8(uint256)` (solidity/test_unsafe_downcast.sol#L42-L47) is never used and should be removed

- `UnsafeDowncast.toUint256(int256)` (solidity/test_unsafe_downcast.sol#L49-L54) is never used and should be removed

- `UnsafeDowncast.toInt8(int256)` (solidity/test_unsafe_downcast.sol#L56-L61) is never used and should be removed

- `UnsafeDowncast.toInt256(uint256)` (solidity/test_unsafe_downcast.sol#L63-L68) is never used and should be removed


### recommendation:
Remove unused functions.

### locations:
- solidity/test_unsafe_downcast.sol#L42-L47
- solidity/test_unsafe_downcast.sol#L49-L54
- solidity/test_unsafe_downcast.sol#L56-L61
- solidity/test_unsafe_downcast.sol#L63-L68

### severity:
Optimization

### category:
dead-code

## [Optimization] `internal` functions only called once can be inlined to save gas

### description:

Not inlining costs **20 to 40 gas** because of two extra `JUMP` instructions and additional stack operations needed for function calls.
more detail see [this](https://docs.soliditylang.org/en/v0.8.20/internals/optimizer.html#function-inlining) and [this](https://blog.soliditylang.org/2021/03/02/saving-gas-with-simple-inliner/)
        

**There is `1` instance of this issue:**

- `UnsafeDowncast.toUint128(uint256)` (solidity/test_unsafe_downcast.sol#L35-L40) could be inlined to save gas.


### recommendation:
Using inlining replace `internal` function which only called once

### locations:
- solidity/test_unsafe_downcast.sol#L35-L40

### severity:
Optimization

### category:
internal-function-to-inline

## [Optimization] Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead

### description:

> When using elements that are smaller than 32 bytes, your contract’s gas usage may be higher. This is because the EVM operates on 32 bytes at a time. Therefore, if the element is smaller than that, the EVM must use more operations in order to reduce the size of the element from 32 bytes to the desired size.

More detail see [this.](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html)

Each operation involving a `uint8` costs an extra [**22-28 gas**](https://gist.github.com/0xxfu/3672fec07eb3031cd5da14ac015e04a1) (depending on whether the other operand is also a variable of type `uint8`) as compared to ones involving `uint256`, due to the compiler having to clear the higher bits of the memory word before operating on the `uint8`, as well as the associated stack operations of doing so. Use a larger size then downcast where needed


**There are `8` instances of this issue:**

- `uint128 []UnsafeDowncast.ui128` (solidity/test_unsafe_downcast.sol#L3) should be used `uint256/int256`.

- `uint32 []UnsafeDowncast.ui32` (solidity/test_unsafe_downcast.sol#L4) should be used `uint256/int256`.

- `int8 []UnsafeDowncast.i8` (solidity/test_unsafe_downcast.sol#L7) should be used `uint256/int256`.

- `uint32 []UnsafeDowncast.bad2(uint128).` (solidity/test_unsafe_downcast.sol#L23) should be used `uint256/int256`.

- `uint128 []UnsafeDowncast.bad2(uint128).a` (solidity/test_unsafe_downcast.sol#L23) should be used `uint256/int256`.

- `uint128 []UnsafeDowncast.toUint128(uint256).` (solidity/test_unsafe_downcast.sol#L35) should be used `uint256/int256`.

- `uint8 []UnsafeDowncast.toUint8(uint256).` (solidity/test_unsafe_downcast.sol#L42) should be used `uint256/int256`.

- `int8 []UnsafeDowncast.toInt8(int256).downcasted` (solidity/test_unsafe_downcast.sol#L56) should be used `uint256/int256`.


### recommendation:

Using `uint256/int256` replace `uint128/uint64/uint32/uint16/uint8` or `int128/int64/int32/int16/int8`


### locations:
- solidity/test_unsafe_downcast.sol#L3
- solidity/test_unsafe_downcast.sol#L4
- solidity/test_unsafe_downcast.sol#L7
- solidity/test_unsafe_downcast.sol#L23
- solidity/test_unsafe_downcast.sol#L23
- solidity/test_unsafe_downcast.sol#L35
- solidity/test_unsafe_downcast.sol#L42
- solidity/test_unsafe_downcast.sol#L56

### severity:
Optimization

### category:
smaller-uint-int

## [Optimization] Use indexed events for value types as they are less costly compared to non-indexed ones

### description:

Using the `indexed` keyword for [value types](https://docs.soliditylang.org/en/v0.8.20/types.html#value-types) (`bool/int/address/string/bytes`) saves gas costs, as seen in [this example](https://gist.github.com/0xxfu/c292a65ecb61cae6fd2090366ea0877e).

However, this is only the case for value types, whereas indexing [reference types](https://docs.soliditylang.org/en/v0.8.20/types.html#reference-types) (`array/struct`) are more expensive than their unindexed version.


**There is `1` instance of this issue:**

- The following variables should be indexed in `UnsafeDowncast.Transmitted(uint32)` (solidity/test_unsafe_downcast.sol#L8):

	- `ue` (solidity/test_unsafe_downcast.sol#L8)


### recommendation:

Using the `indexed` keyword for values types `bool/int/address/string/bytes` in event


### locations:
- solidity/test_unsafe_downcast.sol#L8

### severity:
Optimization

### category:
unindexed-event

## [Optimization] Remove or replace unused state variables

### description:

Saves a storage slot. If the variable is assigned a non-zero value, saves Gsset (20000 gas). If it's assigned a zero value, saves Gsreset (2900 gas). If the variable remains unassigned, there is no gas savings unless the variable is public, in which case the compiler-generated non-payable getter deployment cost is saved. If the state variable is overriding an interface's public function, mark the variable as constant or immutable so that it does not use a storage slot


**There are `2` instances of this issue:**

- `UnsafeDowncast.ui256` (solidity/test_unsafe_downcast.sol#L2) is never used.
- `UnsafeDowncast.i8` (solidity/test_unsafe_downcast.sol#L7) is never used.

### recommendation:

Remove or replace the unused state variables


### locations:
- solidity/test_unsafe_downcast.sol#L2
- solidity/test_unsafe_downcast.sol#L7

### severity:
Optimization

### category:
unused-state-variables

## [Optimization] State variables that could be declared constant

### description:
State variables that are not updated following deployment should be declared constant to save gas.

**There are `2` instances of this issue:**

- `UnsafeDowncast.ui256` (solidity/test_unsafe_downcast.sol#L2) should be constant 

- `UnsafeDowncast.i8` (solidity/test_unsafe_downcast.sol#L7) should be constant 


### recommendation:
Add the `constant` attribute to state variables that never change.

### locations:
- solidity/test_unsafe_downcast.sol#L2
- solidity/test_unsafe_downcast.sol#L7

### severity:
Optimization

### category:
constable-states
