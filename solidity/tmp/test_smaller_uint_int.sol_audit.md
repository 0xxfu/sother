## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Variable names too similar | 2 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead | 21 |
| [G-1] | Remove or replace unused state variables | 12 |
| [G-2] | Remove unused parameter variables | 1 |
| [G-3] | Remove unused local variables | 1 |
| [G-4] | State variables that could be declared constant | 12 |
| [G-5] | State variables that could be declared constant | 12 |



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

## [Informational] Variable names too similar

### description
Detect variables with names that are too similar.

**There are `2` instances of this issue:**

- Variable [SmallerUintInt.stateUint16](solidity/tmp/test_smaller_uint_int.sol#L8) is too similar to [SmallerUintInt.stateUint64](solidity/tmp/test_smaller_uint_int.sol#L6)

- Variable [SmallerUintInt.bad(uint8).localUint16](solidity/tmp/test_smaller_uint_int.sol#L23) is too similar to [SmallerUintInt.bad(uint8).localUint64](solidity/tmp/test_smaller_uint_int.sol#L21)

#### Exploit scenario
Bob uses several variables with similar names. As a result, his code is difficult to review.

### recommendation
Prevent variables from having similar names.

### locations
- solidity/tmp/test_smaller_uint_int.sol#L8
- solidity/tmp/test_smaller_uint_int.sol#L23

### severity
Informational

### category
similar-names

### confidence
Medium

## [Optimization] Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead

### description

> When using elements that are smaller than 32 bytes, your contract’s gas usage may be higher. This is because the EVM operates on 32 bytes at a time. Therefore, if the element is smaller than that, the EVM must use more operations in order to reduce the size of the element from 32 bytes to the desired size.

More detail see [this.](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html)

Each operation involving a `uint8` costs an extra [**22-28 gas**](https://gist.github.com/0xxfu/3672fec07eb3031cd5da14ac015e04a1) (depending on whether the other operand is also a variable of type `uint8`) as compared to ones involving `uint256`, due to the compiler having to clear the higher bits of the memory word before operating on the `uint8`, as well as the associated stack operations of doing so. Use a larger size then downcast where needed


**There are `21` instances of this issue:**

- `uint128 `[SmallerUintInt.stateUint128](solidity/tmp/test_smaller_uint_int.sol#L5) should be used `uint256/int256`.

- `uint64 `[SmallerUintInt.stateUint64](solidity/tmp/test_smaller_uint_int.sol#L6) should be used `uint256/int256`.

- `uint32 `[SmallerUintInt.stateUint32](solidity/tmp/test_smaller_uint_int.sol#L7) should be used `uint256/int256`.

- `uint16 `[SmallerUintInt.stateUint16](solidity/tmp/test_smaller_uint_int.sol#L8) should be used `uint256/int256`.

- `uint8 `[SmallerUintInt.stateUint8](solidity/tmp/test_smaller_uint_int.sol#L9) should be used `uint256/int256`.

- `int128 `[SmallerUintInt.stateint128](solidity/tmp/test_smaller_uint_int.sol#L12) should be used `uint256/int256`.

- `int64 `[SmallerUintInt.stateint64](solidity/tmp/test_smaller_uint_int.sol#L13) should be used `uint256/int256`.

- `int32 `[SmallerUintInt.stateint32](solidity/tmp/test_smaller_uint_int.sol#L14) should be used `uint256/int256`.

- `int16 `[SmallerUintInt.stateint16](solidity/tmp/test_smaller_uint_int.sol#L15) should be used `uint256/int256`.

- `int8 `[SmallerUintInt.stateint8](solidity/tmp/test_smaller_uint_int.sol#L16) should be used `uint256/int256`.

- `uint8 `[SmallerUintInt.bad(uint8)._localUint8](solidity/tmp/test_smaller_uint_int.sol#L18) should be used `uint256/int256`.

- `uint128 `[SmallerUintInt.bad(uint8).localUint128](solidity/tmp/test_smaller_uint_int.sol#L20) should be used `uint256/int256`.

- `uint64 `[SmallerUintInt.bad(uint8).localUint64](solidity/tmp/test_smaller_uint_int.sol#L21) should be used `uint256/int256`.

- `uint32 `[SmallerUintInt.bad(uint8).localUint32](solidity/tmp/test_smaller_uint_int.sol#L22) should be used `uint256/int256`.

- `uint16 `[SmallerUintInt.bad(uint8).localUint16](solidity/tmp/test_smaller_uint_int.sol#L23) should be used `uint256/int256`.

- `uint8 `[SmallerUintInt.bad(uint8).localUint8](solidity/tmp/test_smaller_uint_int.sol#L24) should be used `uint256/int256`.

- `int128 `[SmallerUintInt.bad(uint8).localint128](solidity/tmp/test_smaller_uint_int.sol#L27) should be used `uint256/int256`.

- `int64 `[SmallerUintInt.bad(uint8).localint64](solidity/tmp/test_smaller_uint_int.sol#L28) should be used `uint256/int256`.

- `int32 `[SmallerUintInt.bad(uint8).localint32](solidity/tmp/test_smaller_uint_int.sol#L29) should be used `uint256/int256`.

- `int16 `[SmallerUintInt.bad(uint8).localint16](solidity/tmp/test_smaller_uint_int.sol#L30) should be used `uint256/int256`.

- `int8 `[SmallerUintInt.bad(uint8).localint8](solidity/tmp/test_smaller_uint_int.sol#L31) should be used `uint256/int256`.


### recommendation

Using `uint256/int256` replace `uint128/uint64/uint32/uint16/uint8` or `int128/int64/int32/int16/int8`


### locations
- solidity/tmp/test_smaller_uint_int.sol#L5
- solidity/tmp/test_smaller_uint_int.sol#L6
- solidity/tmp/test_smaller_uint_int.sol#L7
- solidity/tmp/test_smaller_uint_int.sol#L8
- solidity/tmp/test_smaller_uint_int.sol#L9
- solidity/tmp/test_smaller_uint_int.sol#L12
- solidity/tmp/test_smaller_uint_int.sol#L13
- solidity/tmp/test_smaller_uint_int.sol#L14
- solidity/tmp/test_smaller_uint_int.sol#L15
- solidity/tmp/test_smaller_uint_int.sol#L16
- solidity/tmp/test_smaller_uint_int.sol#L18
- solidity/tmp/test_smaller_uint_int.sol#L20
- solidity/tmp/test_smaller_uint_int.sol#L21
- solidity/tmp/test_smaller_uint_int.sol#L22
- solidity/tmp/test_smaller_uint_int.sol#L23
- solidity/tmp/test_smaller_uint_int.sol#L24
- solidity/tmp/test_smaller_uint_int.sol#L27
- solidity/tmp/test_smaller_uint_int.sol#L28
- solidity/tmp/test_smaller_uint_int.sol#L29
- solidity/tmp/test_smaller_uint_int.sol#L30
- solidity/tmp/test_smaller_uint_int.sol#L31

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


**There are `12` instances of this issue:**

- [SmallerUintInt.stateUint256](solidity/tmp/test_smaller_uint_int.sol#L4) is never used.
- [SmallerUintInt.stateUint128](solidity/tmp/test_smaller_uint_int.sol#L5) is never used.
- [SmallerUintInt.stateUint64](solidity/tmp/test_smaller_uint_int.sol#L6) is never used.
- [SmallerUintInt.stateUint32](solidity/tmp/test_smaller_uint_int.sol#L7) is never used.
- [SmallerUintInt.stateUint16](solidity/tmp/test_smaller_uint_int.sol#L8) is never used.
- [SmallerUintInt.stateUint8](solidity/tmp/test_smaller_uint_int.sol#L9) is never used.
- [SmallerUintInt.stateint256](solidity/tmp/test_smaller_uint_int.sol#L11) is never used.
- [SmallerUintInt.stateint128](solidity/tmp/test_smaller_uint_int.sol#L12) is never used.
- [SmallerUintInt.stateint64](solidity/tmp/test_smaller_uint_int.sol#L13) is never used.
- [SmallerUintInt.stateint32](solidity/tmp/test_smaller_uint_int.sol#L14) is never used.
- [SmallerUintInt.stateint16](solidity/tmp/test_smaller_uint_int.sol#L15) is never used.
- [SmallerUintInt.stateint8](solidity/tmp/test_smaller_uint_int.sol#L16) is never used.

### recommendation

Remove or replace the unused state variables


### locations
- solidity/tmp/test_smaller_uint_int.sol#L4
- solidity/tmp/test_smaller_uint_int.sol#L5
- solidity/tmp/test_smaller_uint_int.sol#L6
- solidity/tmp/test_smaller_uint_int.sol#L7
- solidity/tmp/test_smaller_uint_int.sol#L8
- solidity/tmp/test_smaller_uint_int.sol#L9
- solidity/tmp/test_smaller_uint_int.sol#L11
- solidity/tmp/test_smaller_uint_int.sol#L12
- solidity/tmp/test_smaller_uint_int.sol#L13
- solidity/tmp/test_smaller_uint_int.sol#L14
- solidity/tmp/test_smaller_uint_int.sol#L15
- solidity/tmp/test_smaller_uint_int.sol#L16

### severity
Optimization

### category
unused-state-variables

### confidence
High

## [Optimization] Remove unused parameter variables

### description

Unused parameters variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 



**There is `1` instance of this issue:**

- The param variables in [SmallerUintInt.bad(uint8)](solidity/tmp/test_smaller_uint_int.sol#L18-L32) are unused.
	- [SmallerUintInt.bad(uint8)._localUint8](solidity/tmp/test_smaller_uint_int.sol#L18)


### recommendation

Remove the unused parameter variables.


### locations
- solidity/tmp/test_smaller_uint_int.sol#L18-L32

### severity
Optimization

### category
unused-parameter

### confidence
High

## [Optimization] Remove unused local variables

### description

Unused local variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 


**There is `1` instance of this issue:**

- The local variables in [SmallerUintInt.bad(uint8)](solidity/tmp/test_smaller_uint_int.sol#L18-L32) are unused.
	- [SmallerUintInt.bad(uint8).localUint8](solidity/tmp/test_smaller_uint_int.sol#L24)
	- [SmallerUintInt.bad(uint8).localint256](solidity/tmp/test_smaller_uint_int.sol#L26)
	- [SmallerUintInt.bad(uint8).localUint16](solidity/tmp/test_smaller_uint_int.sol#L23)
	- [SmallerUintInt.bad(uint8).localint128](solidity/tmp/test_smaller_uint_int.sol#L27)
	- [SmallerUintInt.bad(uint8).localUint128](solidity/tmp/test_smaller_uint_int.sol#L20)
	- [SmallerUintInt.bad(uint8).localint16](solidity/tmp/test_smaller_uint_int.sol#L30)
	- [SmallerUintInt.bad(uint8).localint8](solidity/tmp/test_smaller_uint_int.sol#L31)
	- [SmallerUintInt.bad(uint8).localUint64](solidity/tmp/test_smaller_uint_int.sol#L21)
	- [SmallerUintInt.bad(uint8).localUint32](solidity/tmp/test_smaller_uint_int.sol#L22)
	- [SmallerUintInt.bad(uint8).localUint256](solidity/tmp/test_smaller_uint_int.sol#L19)
	- [SmallerUintInt.bad(uint8).localint32](solidity/tmp/test_smaller_uint_int.sol#L29)
	- [SmallerUintInt.bad(uint8).localint64](solidity/tmp/test_smaller_uint_int.sol#L28)


### recommendation

Remove the unused local variables.


### locations
- solidity/tmp/test_smaller_uint_int.sol#L18-L32

### severity
Optimization

### category
unused-local-var

### confidence
High

## [Optimization] State variables that could be declared constant

### description
State variables that are not updated following deployment should be declared constant to save gas.

**There are `12` instances of this issue:**

- [SmallerUintInt.stateUint256](solidity/tmp/test_smaller_uint_int.sol#L4) should be constant 

- [SmallerUintInt.stateUint128](solidity/tmp/test_smaller_uint_int.sol#L5) should be constant 

- [SmallerUintInt.stateUint64](solidity/tmp/test_smaller_uint_int.sol#L6) should be constant 

- [SmallerUintInt.stateUint32](solidity/tmp/test_smaller_uint_int.sol#L7) should be constant 

- [SmallerUintInt.stateUint16](solidity/tmp/test_smaller_uint_int.sol#L8) should be constant 

- [SmallerUintInt.stateUint8](solidity/tmp/test_smaller_uint_int.sol#L9) should be constant 

- [SmallerUintInt.stateint256](solidity/tmp/test_smaller_uint_int.sol#L11) should be constant 

- [SmallerUintInt.stateint128](solidity/tmp/test_smaller_uint_int.sol#L12) should be constant 

- [SmallerUintInt.stateint64](solidity/tmp/test_smaller_uint_int.sol#L13) should be constant 

- [SmallerUintInt.stateint32](solidity/tmp/test_smaller_uint_int.sol#L14) should be constant 

- [SmallerUintInt.stateint16](solidity/tmp/test_smaller_uint_int.sol#L15) should be constant 

- [SmallerUintInt.stateint8](solidity/tmp/test_smaller_uint_int.sol#L16) should be constant 


### recommendation
Add the `constant` attribute to state variables that never change.

### locations
- solidity/tmp/test_smaller_uint_int.sol#L4
- solidity/tmp/test_smaller_uint_int.sol#L5
- solidity/tmp/test_smaller_uint_int.sol#L6
- solidity/tmp/test_smaller_uint_int.sol#L7
- solidity/tmp/test_smaller_uint_int.sol#L8
- solidity/tmp/test_smaller_uint_int.sol#L9
- solidity/tmp/test_smaller_uint_int.sol#L11
- solidity/tmp/test_smaller_uint_int.sol#L12
- solidity/tmp/test_smaller_uint_int.sol#L13
- solidity/tmp/test_smaller_uint_int.sol#L14
- solidity/tmp/test_smaller_uint_int.sol#L15
- solidity/tmp/test_smaller_uint_int.sol#L16

### severity
Optimization

### category
constable-states

### confidence
High

## [Optimization] State variables that could be declared constant

### description
Constant state variables should be declared constant to save gas.

**There are `12` instances of this issue:**

- [SmallerUintInt.stateUint256](solidity/tmp/test_smaller_uint_int.sol#L4) should be constant

- [SmallerUintInt.stateUint128](solidity/tmp/test_smaller_uint_int.sol#L5) should be constant

- [SmallerUintInt.stateUint64](solidity/tmp/test_smaller_uint_int.sol#L6) should be constant

- [SmallerUintInt.stateUint32](solidity/tmp/test_smaller_uint_int.sol#L7) should be constant

- [SmallerUintInt.stateUint16](solidity/tmp/test_smaller_uint_int.sol#L8) should be constant

- [SmallerUintInt.stateUint8](solidity/tmp/test_smaller_uint_int.sol#L9) should be constant

- [SmallerUintInt.stateint256](solidity/tmp/test_smaller_uint_int.sol#L11) should be constant

- [SmallerUintInt.stateint128](solidity/tmp/test_smaller_uint_int.sol#L12) should be constant

- [SmallerUintInt.stateint64](solidity/tmp/test_smaller_uint_int.sol#L13) should be constant

- [SmallerUintInt.stateint32](solidity/tmp/test_smaller_uint_int.sol#L14) should be constant

- [SmallerUintInt.stateint16](solidity/tmp/test_smaller_uint_int.sol#L15) should be constant

- [SmallerUintInt.stateint8](solidity/tmp/test_smaller_uint_int.sol#L16) should be constant


### recommendation
Add the `constant` attributes to state variables that never change.

### locations
- solidity/tmp/test_smaller_uint_int.sol#L4
- solidity/tmp/test_smaller_uint_int.sol#L5
- solidity/tmp/test_smaller_uint_int.sol#L6
- solidity/tmp/test_smaller_uint_int.sol#L7
- solidity/tmp/test_smaller_uint_int.sol#L8
- solidity/tmp/test_smaller_uint_int.sol#L9
- solidity/tmp/test_smaller_uint_int.sol#L11
- solidity/tmp/test_smaller_uint_int.sol#L12
- solidity/tmp/test_smaller_uint_int.sol#L13
- solidity/tmp/test_smaller_uint_int.sol#L14
- solidity/tmp/test_smaller_uint_int.sol#L15
- solidity/tmp/test_smaller_uint_int.sol#L16

### severity
Optimization

### category
state-should-be-constant

### confidence
High
