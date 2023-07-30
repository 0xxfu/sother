## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Division by zero not prevented | 9 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Magic Number | 5 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Using custom errors replace `require` or `assert` | 2 |
| [G-1] | Using `x >> constant(uint)` with the right shift operator is a more gas-efficient | 1 |
| [G-2] | The result of function calls should be cached rather than re-calling the function | 3 |



## [Low] Division by zero not prevented

### description:

In Solidity, transactions are reverted with the "division by zero" error
message when a division by zero is attempted.
Although divisions by zero will result in reversions, 
they will not have error messages, 
making failed transaction more difficult to debug by users.

Consider actively preventing divisions by zero with appropriate `revert` statements that 
have informative and user-friendly error messages.


**There are `9` instances of this issue:**

- [10 / a](solidity/division_by_zero.sol#L3) possible divisions by `0` can be performed.

- [f0() / a](solidity/division_by_zero.sol#L5) possible divisions by `0` can be performed.

- [10 / (a * b)](solidity/division_by_zero.sol#L7) possible divisions by `0` can be performed.

- [10 / (f0() * a)](solidity/division_by_zero.sol#L9) possible divisions by `0` can be performed.

- [10 / (f0() * a - 100)](solidity/division_by_zero.sol#L11) possible divisions by `0` can be performed.

- [f0() / a - 1](solidity/division_by_zero.sol#L13) possible divisions by `0` can be performed.

- [10 / (a + 1)](solidity/division_by_zero.sol#L45) possible divisions by `0` can be performed.

- [10 / (a * b + 1)](solidity/division_by_zero.sol#L47) possible divisions by `0` can be performed.

- [a / (b + 1)](solidity/division_by_zero.sol#L51) possible divisions by `0` can be performed.


### recommendation:

It is recommended to add a sanity check to control whether the borrowed
amount is zero or not.


### locations:
- solidity/division_by_zero.sol#L3
- solidity/division_by_zero.sol#L5
- solidity/division_by_zero.sol#L7
- solidity/division_by_zero.sol#L9
- solidity/division_by_zero.sol#L11
- solidity/division_by_zero.sol#L13
- solidity/division_by_zero.sol#L45
- solidity/division_by_zero.sol#L47
- solidity/division_by_zero.sol#L51

### severity:
Low

### category:
division-by-zero

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

## [Informational] Magic Number

### description:
Values should be assigned to variables

**There are `5` instances of this issue:**

- Function [DivisionByZero.bad0(uint256,uint256)](solidity/division_by_zero.sol#L2-L14) contains magic numbers: 10, 10, 10, 10

- Function [DivisionByZero.notBad0(uint256,uint256)](solidity/division_by_zero.sol#L16-L30) contains magic numbers: 10, 10, 10

- Function [DivisionByZero.notBad1(uint256,uint256)](solidity/division_by_zero.sol#L32-L42) contains magic numbers: 10, 10, 10

- Function [DivisionByZero.notBad2(uint256,uint256)](solidity/division_by_zero.sol#L44-L52) contains magic numbers: 10, 10

- Function [DivisionByZero.f0()](solidity/division_by_zero.sol#L54-L56) contains magic number: 10

#### Exploit scenario
-

### recommendation:
Assign values to variables

### locations:
- solidity/division_by_zero.sol#L2-L14
- solidity/division_by_zero.sol#L16-L30
- solidity/division_by_zero.sol#L32-L42
- solidity/division_by_zero.sol#L44-L52
- solidity/division_by_zero.sol#L54-L56

### severity:
Informational

### category:
pess-magic-number

## [Optimization] Using custom errors replace `require` or `assert`

### description:

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `2` instances of this issue:**

- [require(bool)(a != 0)](solidity/division_by_zero.sol#L33) should use custom error to save gas.

- [require(bool)(b != 0)](solidity/division_by_zero.sol#L34) should use custom error to save gas.


### recommendation:

Using custom errors replace `require` or `assert`.


### locations:
- solidity/division_by_zero.sol#L33
- solidity/division_by_zero.sol#L34

### severity:
Optimization

### category:
use-custom-error

## [Optimization] Using `x >> constant(uint)` with the right shift operator is a more gas-efficient

### description:

`<x> / 2` is the same as `<x> >> 1`. While the compiler uses the `SHR` opcode to accomplish both, 
the version that uses division incurs an overhead of [**20 gas**](https://gist.github.com/0xxfu/84e3727f28e01f9b628836d5bf55d0cc) 
due to `JUMP`s to and from a compiler utility function that introduces checks which can 
be avoided by using `unchecked {}` around the division by two



**There is `1` instance of this issue:**

- [a / 1](solidity/division_by_zero.sol#L49) should use right shift `>>` operator to save gas.


### recommendation:

Using bit shifting (`>>` operator) replace division divided by constant.


### locations:
- solidity/division_by_zero.sol#L49

### severity:
Optimization

### category:
divide-by-constant

## [Optimization] The result of function calls should be cached rather than re-calling the function

### description:

The instances below point to the second+ call of the function within a single function


**There are `3` instances of this issue:**

- `DivisionByZero.f0()` called result should be cached with local variable in [DivisionByZero.bad0(uint256,uint256)](solidity/division_by_zero.sol#L2-L14), It is called more than once:
	- [f0() / a - 1](solidity/division_by_zero.sol#L13)
	- [10 / (f0() * a)](solidity/division_by_zero.sol#L9)
	- [10 / (f0() * a - 100)](solidity/division_by_zero.sol#L11)
	- [f0() / a](solidity/division_by_zero.sol#L5)

- `DivisionByZero.f0()` called result should be cached with local variable in [DivisionByZero.notBad0(uint256,uint256)](solidity/division_by_zero.sol#L16-L30), It is called more than once:
	- [f0() / a](solidity/division_by_zero.sol#L25)
	- [10 / (f0() * a)](solidity/division_by_zero.sol#L29)

- `DivisionByZero.f0()` called result should be cached with local variable in [DivisionByZero.notBad1(uint256,uint256)](solidity/division_by_zero.sol#L32-L42), It is called more than once:
	- [10 / (f0() * a)](solidity/division_by_zero.sol#L41)
	- [f0() / a](solidity/division_by_zero.sol#L37)


### recommendation:

Using local variable to cache function called result if the same function called more than once.


### locations:
- solidity/division_by_zero.sol#L2-L14
- solidity/division_by_zero.sol#L16-L30
- solidity/division_by_zero.sol#L32-L42

### severity:
Optimization

### category:
cache-call-function-result
