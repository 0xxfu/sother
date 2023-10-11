## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Integer Overflow and Underflow | 11 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Setters should check the input value | 3 |
| [L-1] | Missing Event Setter | 3 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | The result of function calls should be cached rather than re-calling the function | 1 |



## [Medium] Integer Overflow and Underflow

### description

    若不使用OpenZeppelin的SafeMath(或类似的库)检查溢出/下溢，
    如果用户/攻击者能够控制这种算术运算的整数操作数，
    可能会导致漏洞或意外行为。
    Solc v0.8.0为所有算术运算引入了默认的溢出/底溢检查。(见这里和这里)

**There are `11` instances of this issue:**

- bad(uint256) has possible integer overflow/underflow:
	- [a = a + externalPure()](solidity/tmp/test_cache_call_function_result.sol#L6)

- bad(uint256) has possible integer overflow/underflow:
	- [a = a + externalPure()](solidity/tmp/test_cache_call_function_result.sol#L7)

- bad(uint256) has possible integer overflow/underflow:
	- [a = a + publicPure()](solidity/tmp/test_cache_call_function_result.sol#L8)

- bad(uint256) has possible integer overflow/underflow:
	- [state = a + 1](solidity/tmp/test_cache_call_function_result.sol#L9)

- notBad(uint256) has possible integer overflow/underflow:
	- [a = a + internalViewPassParam(a)](solidity/tmp/test_cache_call_function_result.sol#L13)

- notBad(uint256) has possible integer overflow/underflow:
	- [a = a + internalViewPassParam(a)](solidity/tmp/test_cache_call_function_result.sol#L14)

- notBad(uint256) has possible integer overflow/underflow:
	- [state = a + 1](solidity/tmp/test_cache_call_function_result.sol#L15)

- good(uint256) has possible integer overflow/underflow:
	- [a = a + extPure](solidity/tmp/test_cache_call_function_result.sol#L20)

- good(uint256) has possible integer overflow/underflow:
	- [a = a + extPure](solidity/tmp/test_cache_call_function_result.sol#L21)

- good(uint256) has possible integer overflow/underflow:
	- [state = a + 1](solidity/tmp/test_cache_call_function_result.sol#L22)

- internalViewPassParam(uint256) has possible integer overflow/underflow:
	- [x + 1](solidity/tmp/test_cache_call_function_result.sol#L34)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/tmp/test_cache_call_function_result.sol#L6
- solidity/tmp/test_cache_call_function_result.sol#L7
- solidity/tmp/test_cache_call_function_result.sol#L8
- solidity/tmp/test_cache_call_function_result.sol#L9
- solidity/tmp/test_cache_call_function_result.sol#L13
- solidity/tmp/test_cache_call_function_result.sol#L14
- solidity/tmp/test_cache_call_function_result.sol#L15
- solidity/tmp/test_cache_call_function_result.sol#L20
- solidity/tmp/test_cache_call_function_result.sol#L21
- solidity/tmp/test_cache_call_function_result.sol#L22
- solidity/tmp/test_cache_call_function_result.sol#L34

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


**There are `3` instances of this issue:**

- [CallFunctionResult.bad(uint256).a](solidity/tmp/test_cache_call_function_result.sol#L5) lacks an upper limit check on :
	- [state = a + 1](solidity/tmp/test_cache_call_function_result.sol#L9)

- [CallFunctionResult.notBad(uint256).a](solidity/tmp/test_cache_call_function_result.sol#L12) lacks an upper limit check on :
	- [state = a + 1](solidity/tmp/test_cache_call_function_result.sol#L15)

- [CallFunctionResult.good(uint256).a](solidity/tmp/test_cache_call_function_result.sol#L18) lacks an upper limit check on :
	- [state = a + 1](solidity/tmp/test_cache_call_function_result.sol#L22)


### recommendation

Add an upper limit check to the setters function.


### locations
- solidity/tmp/test_cache_call_function_result.sol#L5
- solidity/tmp/test_cache_call_function_result.sol#L12
- solidity/tmp/test_cache_call_function_result.sol#L18

### severity
Low

### category
unchecked-setters

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `3` instances of this issue:**

- Setter function [CallFunctionResult.bad(uint256)](solidity/tmp/test_cache_call_function_result.sol#L5-L10) does not emit an event

- Setter function [CallFunctionResult.notBad(uint256)](solidity/tmp/test_cache_call_function_result.sol#L12-L16) does not emit an event

- Setter function [CallFunctionResult.good(uint256)](solidity/tmp/test_cache_call_function_result.sol#L18-L23) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/test_cache_call_function_result.sol#L5-L10
- solidity/tmp/test_cache_call_function_result.sol#L12-L16
- solidity/tmp/test_cache_call_function_result.sol#L18-L23

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

## [Optimization] The result of function calls should be cached rather than re-calling the function

### description

The instances below point to the second+ call of the function within a single function


**There is `1` instance of this issue:**

- `CallFunctionResult.externalPure()` called result should be cached with local variable in [CallFunctionResult.bad(uint256)](solidity/tmp/test_cache_call_function_result.sol#L5-L10), It is called more than once:
	- [a = a + externalPure()](solidity/tmp/test_cache_call_function_result.sol#L6)
	- [a = a + externalPure()](solidity/tmp/test_cache_call_function_result.sol#L7)


### recommendation

Using local variable to cache function called result if the same function called more than once.


### locations
- solidity/tmp/test_cache_call_function_result.sol#L5-L10

### severity
Optimization

### category
cache-call-function-result

### confidence
High
