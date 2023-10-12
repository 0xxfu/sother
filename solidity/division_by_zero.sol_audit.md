## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | Integer Overflow and Underflow | 2 |


### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Integer Overflow and Underflow | 7 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Division by zero not prevented | 9 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | .. | 2 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Using custom errors replace `require` or `assert` | 2 |
| [G-1] | Using `x >> constant(uint)` with the right shift operator is a more gas-efficient | 1 |
| [G-2] | The result of function calls should be cached rather than re-calling the function | 3 |



## [High] Integer Overflow and Underflow

### description

    若不使用OpenZeppelin的SafeMath(或类似的库)检查溢出/下溢，
    如果用户/攻击者能够控制这种算术运算的整数操作数，
    可能会导致漏洞或意外行为。
    Solc v0.8.0为所有算术运算引入了默认的溢出/底溢检查。(见这里和这里)

**There are `2` instances of this issue:**

- bad0(uint256,uint256) has possible integer overflow/underflow:
	- [10 / (f0() * a - 100)](solidity/division_by_zero.sol#L11)

- bad0(uint256,uint256) has possible integer overflow/underflow:
	- [f0() / a - 1](solidity/division_by_zero.sol#L13)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/division_by_zero.sol#L11
- solidity/division_by_zero.sol#L13

### severity
High

### category
integer-underflow

### confidence
High

## [Medium] Integer Overflow and Underflow

### description

    若不使用OpenZeppelin的SafeMath(或类似的库)检查溢出/下溢，
    如果用户/攻击者能够控制这种算术运算的整数操作数，
    可能会导致漏洞或意外行为。
    Solc v0.8.0为所有算术运算引入了默认的溢出/底溢检查。(见这里和这里)

**There are `7` instances of this issue:**

- bad0(uint256,uint256) has possible integer overflow/underflow:
	- [10 / (a * b)](solidity/division_by_zero.sol#L7)

- bad0(uint256,uint256) has possible integer overflow/underflow:
	- [10 / (f0() * a)](solidity/division_by_zero.sol#L9)

- notBad0(uint256,uint256) has possible integer overflow/underflow:
	- [10 / (a * b)](solidity/division_by_zero.sol#L27)

- notBad0(uint256,uint256) has possible integer overflow/underflow:
	- [10 / (f0() * a)](solidity/division_by_zero.sol#L29)

- notBad2(uint256,uint256) has possible integer overflow/underflow:
	- [10 / (a + 1)](solidity/division_by_zero.sol#L45)

- notBad2(uint256,uint256) has possible integer overflow/underflow:
	- [10 / (a * b + 1)](solidity/division_by_zero.sol#L47)

- notBad2(uint256,uint256) has possible integer overflow/underflow:
	- [a / (b + 1)](solidity/division_by_zero.sol#L51)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/division_by_zero.sol#L7
- solidity/division_by_zero.sol#L9
- solidity/division_by_zero.sol#L27
- solidity/division_by_zero.sol#L29
- solidity/division_by_zero.sol#L45
- solidity/division_by_zero.sol#L47
- solidity/division_by_zero.sol#L51

### severity
Medium

### category
integer-overflow

### confidence
High

## [Low] Division by zero not prevented

### description

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


### recommendation

It is recommended to add a sanity check to control whether the borrowed
amount is zero or not.


### locations
- solidity/division_by_zero.sol#L3
- solidity/division_by_zero.sol#L5
- solidity/division_by_zero.sol#L7
- solidity/division_by_zero.sol#L9
- solidity/division_by_zero.sol#L11
- solidity/division_by_zero.sol#L13
- solidity/division_by_zero.sol#L45
- solidity/division_by_zero.sol#L47
- solidity/division_by_zero.sol#L51

### severity
Low

### category
division-by-zero

### confidence
High

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

## [Informational] ..

### description
..

**There are `2` instances of this issue:**

- require() missing error messages
	 - [require(bool)(a != 0)](solidity/division_by_zero.sol#L33)

- require() missing error messages
	 - [require(bool)(b != 0)](solidity/division_by_zero.sol#L34)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/division_by_zero.sol#L33
- solidity/division_by_zero.sol#L34

### severity
Informational

### category
error-msg

### confidence
Medium

## [Optimization] Using custom errors replace `require` or `assert`

### description

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `2` instances of this issue:**

- [require(bool)(a != 0)](solidity/division_by_zero.sol#L33) should use custom error to save gas.

- [require(bool)(b != 0)](solidity/division_by_zero.sol#L34) should use custom error to save gas.


### recommendation

Using custom errors replace `require` or `assert`.


### locations
- solidity/division_by_zero.sol#L33
- solidity/division_by_zero.sol#L34

### severity
Optimization

### category
use-custom-error

### confidence
High

## [Optimization] Using `x >> constant(uint)` with the right shift operator is a more gas-efficient

### description

`<x> / 2` is the same as `<x> >> 1`. While the compiler uses the `SHR` opcode to accomplish both, 
the version that uses division incurs an overhead of [**20 gas**](https://gist.github.com/0xxfu/84e3727f28e01f9b628836d5bf55d0cc) 
due to `JUMP`s to and from a compiler utility function that introduces checks which can 
be avoided by using `unchecked {}` around the division by two



**There is `1` instance of this issue:**

- [a / 1](solidity/division_by_zero.sol#L49) should use right shift `>>` operator to save gas.


### recommendation

Using bit shifting (`>>` operator) replace division divided by constant.


### locations
- solidity/division_by_zero.sol#L49

### severity
Optimization

### category
divide-by-constant

### confidence
High

## [Optimization] The result of function calls should be cached rather than re-calling the function

### description

The instances below point to the second+ call of the function within a single function


**There are `3` instances of this issue:**

- `DivisionByZero.f0()` called result should be cached with local variable in [DivisionByZero.bad0(uint256,uint256)](solidity/division_by_zero.sol#L2-L14), It is called more than once:
	- [10 / (f0() * a - 100)](solidity/division_by_zero.sol#L11)
	- [f0() / a](solidity/division_by_zero.sol#L5)
	- [f0() / a - 1](solidity/division_by_zero.sol#L13)
	- [10 / (f0() * a)](solidity/division_by_zero.sol#L9)

- `DivisionByZero.f0()` called result should be cached with local variable in [DivisionByZero.notBad0(uint256,uint256)](solidity/division_by_zero.sol#L16-L30), It is called more than once:
	- [10 / (f0() * a)](solidity/division_by_zero.sol#L29)
	- [f0() / a](solidity/division_by_zero.sol#L25)

- `DivisionByZero.f0()` called result should be cached with local variable in [DivisionByZero.notBad1(uint256,uint256)](solidity/division_by_zero.sol#L32-L42), It is called more than once:
	- [f0() / a](solidity/division_by_zero.sol#L37)
	- [10 / (f0() * a)](solidity/division_by_zero.sol#L41)


### recommendation

Using local variable to cache function called result if the same function called more than once.


### locations
- solidity/division_by_zero.sol#L2-L14
- solidity/division_by_zero.sol#L16-L30
- solidity/division_by_zero.sol#L32-L42

### severity
Optimization

### category
cache-call-function-result

### confidence
High
