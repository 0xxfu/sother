## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Integer Overflow and Underflow | 6 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Setters should check the input value | 4 |
| [L-1] | Missing Event Setter | 4 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | `<x> += <y>` costs more gas than `<x> = <x> + <y>` for state variables | 1 |
| [G-1] | `internal` functions only called once can be inlined to save gas | 3 |



## [Medium] Integer Overflow and Underflow

### description

    若不使用OpenZeppelin的SafeMath(或类似的库)检查溢出/下溢，
    如果用户/攻击者能够控制这种算术运算的整数操作数，
    可能会导致漏洞或意外行为。
    Solc v0.8.0为所有算术运算引入了默认的溢出/底溢检查。(见这里和这里)

**There are `6` instances of this issue:**

- externalFunction(uint256) has possible integer overflow/underflow:
	- [state1 = abc + internalFunction(abc)](solidity/tmp/test_internal_function_to_inline.sol#L6)

- externalFunction2(uint256) has possible integer overflow/underflow:
	- [state1 = abc + internalFunction2(abc)](solidity/tmp/test_internal_function_to_inline.sol#L11)

- internalFunction(uint256) has possible integer overflow/underflow:
	- [xyz + 1](solidity/tmp/test_internal_function_to_inline.sol#L24)

- internalFunction2(uint256) has possible integer overflow/underflow:
	- [xyz + 1](solidity/tmp/test_internal_function_to_inline.sol#L28)

- internalFunction3(uint256) has possible integer overflow/underflow:
	- [xyz + 1](solidity/tmp/test_internal_function_to_inline.sol#L32)

- internalFunction4(uint256) has possible integer overflow/underflow:
	- [xyz + 1](solidity/tmp/test_internal_function_to_inline.sol#L36)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/tmp/test_internal_function_to_inline.sol#L6
- solidity/tmp/test_internal_function_to_inline.sol#L11
- solidity/tmp/test_internal_function_to_inline.sol#L24
- solidity/tmp/test_internal_function_to_inline.sol#L28
- solidity/tmp/test_internal_function_to_inline.sol#L32
- solidity/tmp/test_internal_function_to_inline.sol#L36

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


**There are `4` instances of this issue:**

- [InternalFunctionToInline.externalFunction(uint256).abc](solidity/tmp/test_internal_function_to_inline.sol#L5) lacks an upper limit check on :
	- [state1 = abc + internalFunction(abc)](solidity/tmp/test_internal_function_to_inline.sol#L6)
	- [state1 = state1 + internalFunction2(abc)](solidity/tmp/test_internal_function_to_inline.sol#L7)

- [InternalFunctionToInline.externalFunction2(uint256).abc](solidity/tmp/test_internal_function_to_inline.sol#L10) lacks an upper limit check on :
	- [state1 = abc + internalFunction2(abc)](solidity/tmp/test_internal_function_to_inline.sol#L11)

- [InternalFunctionToInline.externalFunction3(uint256).abc](solidity/tmp/test_internal_function_to_inline.sol#L14) lacks an upper limit check on :
	- [state1 = state1 + internalFunction2(abc)](solidity/tmp/test_internal_function_to_inline.sol#L15)

- [InternalFunctionToInline.externalFunction4(uint256).abc](solidity/tmp/test_internal_function_to_inline.sol#L19) lacks an upper limit check on :
	- [state1 += internalFunction4(abc)](solidity/tmp/test_internal_function_to_inline.sol#L20)


### recommendation

Add an upper limit check to the setters function.


### locations
- solidity/tmp/test_internal_function_to_inline.sol#L5
- solidity/tmp/test_internal_function_to_inline.sol#L10
- solidity/tmp/test_internal_function_to_inline.sol#L14
- solidity/tmp/test_internal_function_to_inline.sol#L19

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

- Setter function [InternalFunctionToInline.externalFunction(uint256)](solidity/tmp/test_internal_function_to_inline.sol#L5-L8) does not emit an event

- Setter function [InternalFunctionToInline.externalFunction2(uint256)](solidity/tmp/test_internal_function_to_inline.sol#L10-L12) does not emit an event

- Setter function [InternalFunctionToInline.externalFunction3(uint256)](solidity/tmp/test_internal_function_to_inline.sol#L14-L17) does not emit an event

- Setter function [InternalFunctionToInline.externalFunction4(uint256)](solidity/tmp/test_internal_function_to_inline.sol#L19-L21) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/test_internal_function_to_inline.sol#L5-L8
- solidity/tmp/test_internal_function_to_inline.sol#L10-L12
- solidity/tmp/test_internal_function_to_inline.sol#L14-L17
- solidity/tmp/test_internal_function_to_inline.sol#L19-L21

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

## [Optimization] `<x> += <y>` costs more gas than `<x> = <x> + <y>` for state variables

### description
Using the addition operator instead of plus-equals saves **[113 gas](https://gist.github.com/0xxfu/86ae4bdd07d7db169cea110dba5a5af4)**

**There is `1` instance of this issue:**

- should use arithmetic operator `=` replace `+=` in [state1 += internalFunction4(abc)](solidity/tmp/test_internal_function_to_inline.sol#L20)

### recommendation
Using arithmetic operator `=` replace assignment operator `+=` or `-=` 

### locations
- solidity/tmp/test_internal_function_to_inline.sol#L20

### severity
Optimization

### category
assignment-left-operation

### confidence
High

## [Optimization] `internal` functions only called once can be inlined to save gas

### description

Not inlining costs **20 to 40 gas** because of two extra `JUMP` instructions and additional stack operations needed for function calls.
more detail see [this](https://docs.soliditylang.org/en/v0.8.20/internals/optimizer.html#function-inlining) and [this](https://blog.soliditylang.org/2021/03/02/saving-gas-with-simple-inliner/)
        

**There are `3` instances of this issue:**

- [InternalFunctionToInline.internalFunction(uint256)](solidity/tmp/test_internal_function_to_inline.sol#L23-L25) could be inlined to save gas.

- [InternalFunctionToInline.internalFunction3(uint256)](solidity/tmp/test_internal_function_to_inline.sol#L31-L33) could be inlined to save gas.

- [InternalFunctionToInline.internalFunction4(uint256)](solidity/tmp/test_internal_function_to_inline.sol#L35-L37) could be inlined to save gas.


### recommendation
Using inlining replace `internal` function which only called once

### locations
- solidity/tmp/test_internal_function_to_inline.sol#L23-L25
- solidity/tmp/test_internal_function_to_inline.sol#L31-L33
- solidity/tmp/test_internal_function_to_inline.sol#L35-L37

### severity
Optimization

### category
internal-function-to-inline

### confidence
High
