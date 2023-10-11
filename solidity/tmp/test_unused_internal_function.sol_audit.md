## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Integer Overflow and Underflow | 2 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Setters should check the input value | 1 |
| [L-1] | Missing Event Setter | 2 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Remove unused parameter variables | 1 |
| [G-1] | Dead-code: functions not used should be removed to save deployment gas | 1 |



## [Medium] Integer Overflow and Underflow

### description

    若不使用OpenZeppelin的SafeMath(或类似的库)检查溢出/下溢，
    如果用户/攻击者能够控制这种算术运算的整数操作数，
    可能会导致漏洞或意外行为。
    Solc v0.8.0为所有算术运算引入了默认的溢出/底溢检查。(见这里和这里)

**There are `2` instances of this issue:**

- good(uint256) has possible integer overflow/underflow:
	- [state = state + a](solidity/tmp/test_unused_internal_function.sol#L11)

- internalUsed(uint256) has possible integer overflow/underflow:
	- [state + a](solidity/tmp/test_unused_internal_function.sol#L16)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/tmp/test_unused_internal_function.sol#L11
- solidity/tmp/test_unused_internal_function.sol#L16

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


**There is `1` instance of this issue:**

- [UnusedInternalFunction.good(uint256).a](solidity/tmp/test_unused_internal_function.sol#L10) lacks an upper limit check on :
	- [state = internalUsed(a) + state](solidity/tmp/test_unused_internal_function.sol#L12)
	- [state = state + a](solidity/tmp/test_unused_internal_function.sol#L11)


### recommendation

Add an upper limit check to the setters function.


### locations
- solidity/tmp/test_unused_internal_function.sol#L10

### severity
Low

### category
unchecked-setters

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `2` instances of this issue:**

- Setter function [UnusedInternalFunction.bad(uint256)](solidity/tmp/test_unused_internal_function.sol#L6-L8) does not emit an event

- Setter function [UnusedInternalFunction.good(uint256)](solidity/tmp/test_unused_internal_function.sol#L10-L13) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/test_unused_internal_function.sol#L6-L8
- solidity/tmp/test_unused_internal_function.sol#L10-L13

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

## [Optimization] Remove unused parameter variables

### description

Unused parameters variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 



**There is `1` instance of this issue:**

- The param variables in [UnusedInternalFunction.bad(uint256)](solidity/tmp/test_unused_internal_function.sol#L6-L8) are unused.
	- [UnusedInternalFunction.bad(uint256).a](solidity/tmp/test_unused_internal_function.sol#L6)


### recommendation

Remove the unused parameter variables.


### locations
- solidity/tmp/test_unused_internal_function.sol#L6-L8

### severity
Optimization

### category
unused-parameter

### confidence
High

## [Optimization] Dead-code: functions not used should be removed to save deployment gas

### description
Functions that are not sued.

**There is `1` instance of this issue:**

- [UnusedInternalFunction.bad(uint256)](solidity/tmp/test_unused_internal_function.sol#L6-L8) is never used and should be removed


### recommendation
Remove unused functions.

### locations
- solidity/tmp/test_unused_internal_function.sol#L6-L8

### severity
Optimization

### category
dead-code

### confidence
High
