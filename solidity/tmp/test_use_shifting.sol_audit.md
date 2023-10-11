## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Divide before multiply | 1 |
| [M-1] | Integer Overflow and Underflow | 6 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Setters should check the input value | 6 |
| [L-1] | Missing Event Setter | 4 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | .. | 3 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Using custom errors replace `require` or `assert` | 3 |
| [G-1] | Using `x >> constant(uint)` with the right shift operator is a more gas-efficient | 3 |
| [G-2] | Multiplications of powers of 2 can be replaced by a left shift operation to save gas | 2 |



## [Medium] Divide before multiply

### description
Solidity's integer division truncates. Thus, performing division before multiplication can lead to precision loss.

**There is `1` instance of this issue:**

- [DivVsShr.bad(uint256)](solidity/tmp/test_use_shifting.sol#L16-L26) performs a multiplication on the result of a division:
	- [result = a / result](solidity/tmp/test_use_shifting.sol#L22)
	- [result = result * 2](solidity/tmp/test_use_shifting.sol#L23)

#### Exploit scenario

```solidity
contract A {
	function f(uint n) public {
        coins = (oldSupply / n) * interest;
    }
}
```
If `n` is greater than `oldSupply`, `coins` will be zero. For example, with `oldSupply = 5; n = 10, interest = 2`, coins will be zero.  
If `(oldSupply * interest / n)` was used, `coins` would have been `1`.   
In general, it's usually a good idea to re-arrange arithmetic to perform multiplication before division, unless the limit of a smaller type makes this dangerous.

### recommendation
Consider ordering multiplication before division.

### locations
- solidity/tmp/test_use_shifting.sol#L16-L26

### severity
Medium

### category
divide-before-multiply

### confidence
Medium

## [Medium] Integer Overflow and Underflow

### description

    若不使用OpenZeppelin的SafeMath(或类似的库)检查溢出/下溢，
    如果用户/攻击者能够控制这种算术运算的整数操作数，
    可能会导致漏洞或意外行为。
    Solc v0.8.0为所有算术运算引入了默认的溢出/底溢检查。(见这里和这里)

**There are `6` instances of this issue:**

- bad(uint256) has possible integer overflow/underflow:
	- [result = result * 2](solidity/tmp/test_use_shifting.sol#L23)

- bad(uint256) has possible integer overflow/underflow:
	- [b = x ** 10](solidity/tmp/test_use_shifting.sol#L44)

- bad(uint256) has possible integer overflow/underflow:
	- [c = 2 ** x](solidity/tmp/test_use_shifting.sol#L45)

- bad(uint256) has possible integer overflow/underflow:
	- [state = a + b + c](solidity/tmp/test_use_shifting.sol#L46)

- good(uint256) has possible integer overflow/underflow:
	- [b = x ** 10](solidity/tmp/test_use_shifting.sol#L51)

- good(uint256) has possible integer overflow/underflow:
	- [state = a + b + c](solidity/tmp/test_use_shifting.sol#L53)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/tmp/test_use_shifting.sol#L23
- solidity/tmp/test_use_shifting.sol#L44
- solidity/tmp/test_use_shifting.sol#L45
- solidity/tmp/test_use_shifting.sol#L46
- solidity/tmp/test_use_shifting.sol#L51
- solidity/tmp/test_use_shifting.sol#L53

### severity
Medium

### category
integer-overflow

### confidence
High

## [Low] Setters should check the input value

### description

Setters should have initial value check to prevent assigning wrong value to the variable. 
Assignment of wrong value can lead to unexpected behavior of the contract.


**There are `6` instances of this issue:**

- [DivVsShr.good(uint256).result](solidity/tmp/test_use_shifting.sol#L10) lacks an upper limit check on :
	- [state = result](solidity/tmp/test_use_shifting.sol#L12)

- [DivVsShr.bad(uint256).result](solidity/tmp/test_use_shifting.sol#L18) lacks an upper limit check on :
	- [state = result](solidity/tmp/test_use_shifting.sol#L25)

- [MulPower.bad(uint256).b](solidity/tmp/test_use_shifting.sol#L44) lacks an upper limit check on :
	- [state = a + b + c](solidity/tmp/test_use_shifting.sol#L46)

- [MulPower.bad(uint256).c](solidity/tmp/test_use_shifting.sol#L45) lacks an upper limit check on :
	- [state = a + b + c](solidity/tmp/test_use_shifting.sol#L46)

- [MulPower.good(uint256).b](solidity/tmp/test_use_shifting.sol#L51) lacks an upper limit check on :
	- [state = a + b + c](solidity/tmp/test_use_shifting.sol#L53)

- [MulPower.good(uint256).c](solidity/tmp/test_use_shifting.sol#L52) lacks an upper limit check on :
	- [state = a + b + c](solidity/tmp/test_use_shifting.sol#L53)


### recommendation

Add an upper limit check to the setters function.


### locations
- solidity/tmp/test_use_shifting.sol#L10
- solidity/tmp/test_use_shifting.sol#L18
- solidity/tmp/test_use_shifting.sol#L44
- solidity/tmp/test_use_shifting.sol#L45
- solidity/tmp/test_use_shifting.sol#L51
- solidity/tmp/test_use_shifting.sol#L52

### severity
Low

### category
unchecked-setters

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `4` instances of this issue:**

- Setter function [DivVsShr.good(uint256)](solidity/tmp/test_use_shifting.sol#L8-L13) does not emit an event

- Setter function [DivVsShr.bad(uint256)](solidity/tmp/test_use_shifting.sol#L16-L26) does not emit an event

- Setter function [MulPower.bad(uint256)](solidity/tmp/test_use_shifting.sol#L42-L47) does not emit an event

- Setter function [MulPower.good(uint256)](solidity/tmp/test_use_shifting.sol#L49-L54) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/test_use_shifting.sol#L8-L13
- solidity/tmp/test_use_shifting.sol#L16-L26
- solidity/tmp/test_use_shifting.sol#L42-L47
- solidity/tmp/test_use_shifting.sol#L49-L54

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

## [Informational] ..

### description
..

**There are `3` instances of this issue:**

- require() missing error messages
	 - [require(bool)(x != 0)](solidity/tmp/test_use_shifting.sol#L9)

- require() missing error messages
	 - [require(bool)(x != 0)](solidity/tmp/test_use_shifting.sol#L17)

- require() missing error messages
	 - [require(bool)(x != 0)](solidity/tmp/test_use_shifting.sol#L30)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/tmp/test_use_shifting.sol#L9
- solidity/tmp/test_use_shifting.sol#L17
- solidity/tmp/test_use_shifting.sol#L30

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


**There are `3` instances of this issue:**

- [require(bool)(x != 0)](solidity/tmp/test_use_shifting.sol#L9) should use custom error to save gas.

- [require(bool)(x != 0)](solidity/tmp/test_use_shifting.sol#L17) should use custom error to save gas.

- [require(bool)(x != 0)](solidity/tmp/test_use_shifting.sol#L30) should use custom error to save gas.


### recommendation

Using custom errors replace `require` or `assert`.


### locations
- solidity/tmp/test_use_shifting.sol#L9
- solidity/tmp/test_use_shifting.sol#L17
- solidity/tmp/test_use_shifting.sol#L30

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



**There are `3` instances of this issue:**

- [result = x / 2](solidity/tmp/test_use_shifting.sol#L19) should use right shift `>>` operator to save gas.

- [a = result / 10](solidity/tmp/test_use_shifting.sol#L21) should use right shift `>>` operator to save gas.

- [result = x / 2](solidity/tmp/test_use_shifting.sol#L33) should use right shift `>>` operator to save gas.


### recommendation

Using bit shifting (`>>` operator) replace division divided by constant.


### locations
- solidity/tmp/test_use_shifting.sol#L19
- solidity/tmp/test_use_shifting.sol#L21
- solidity/tmp/test_use_shifting.sol#L33

### severity
Optimization

### category
divide-by-constant

### confidence
High

## [Optimization] Multiplications of powers of 2 can be replaced by a left shift operation to save gas

### description

`1 << x` is the same as `2**x`. 
A multiplication by any number x being a power of 2 can be calculated by shifting to the left. 
While the `EXP` opcode uses [`gas_cost = 10 + 50 * byte_len_exponent`](https://github.com/wolflo/evm-opcodes/blob/main/gas.md#a1-exp), 
the `SHL` opcode only uses 3 gas.



**There are `2` instances of this issue:**

- [a = 2 ** 10](solidity/tmp/test_use_shifting.sol#L43) should use bit shifting (`<<` operator) to save gas.

- [c = 2 ** x](solidity/tmp/test_use_shifting.sol#L45) should use bit shifting (`<<` operator) to save gas.


### recommendation

Using bit shifting (`<<` operator) replace multiplications of powers of 2 `(2**x)`.


### locations
- solidity/tmp/test_use_shifting.sol#L43
- solidity/tmp/test_use_shifting.sol#L45

### severity
Optimization

### category
mul-power-two

### confidence
High
