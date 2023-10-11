## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Integer Overflow and Underflow | 2 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Missing array length equality checks may lead to incorrect or undefined behavior | 2 |
| [L-1] | Missing Event Setter | 2 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Use `calldata` instead of `memory` for function parameters | 1 |



## [Medium] Integer Overflow and Underflow

### description

    若不使用OpenZeppelin的SafeMath(或类似的库)检查溢出/下溢，
    如果用户/攻击者能够控制这种算术运算的整数操作数，
    可能会导致漏洞或意外行为。
    Solc v0.8.0为所有算术运算引入了默认的溢出/底溢检查。(见这里和这里)

**There are `2` instances of this issue:**

- bad(uint256[],uint256[],uint256[]) has possible integer overflow/underflow:
	- [state = a[0] + b[0] + c[0]](solidity/tmp/test_memory_in_parameters.sol#L11)

- good(uint256[],uint256[],uint256[]) has possible integer overflow/underflow:
	- [state = a[0] + b[0] + c[0]](solidity/tmp/test_memory_in_parameters.sol#L20)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/tmp/test_memory_in_parameters.sol#L11
- solidity/tmp/test_memory_in_parameters.sol#L20

### severity
Medium

### category
integer-overflow

### confidence
High

## [Low] Missing array length equality checks may lead to incorrect or undefined behavior

### description

If the length of the arrays are not required to be of the same length, user operations may not be fully executed due to a mismatch in the number of items iterated over, versus the number of items provided in the second array


**There are `2` instances of this issue:**

- Missing check lengths of parameters below in function [MemoryInParameters.bad(uint256[],uint256[],uint256[])](solidity/tmp/test_memory_in_parameters.sol#L5-L12):
	- [MemoryInParameters.bad(uint256[],uint256[],uint256[]).b](solidity/tmp/test_memory_in_parameters.sol#L7)
	- [MemoryInParameters.bad(uint256[],uint256[],uint256[]).c](solidity/tmp/test_memory_in_parameters.sol#L8)
	- [MemoryInParameters.bad(uint256[],uint256[],uint256[]).a](solidity/tmp/test_memory_in_parameters.sol#L6)

- Missing check lengths of parameters below in function [MemoryInParameters.good(uint256[],uint256[],uint256[])](solidity/tmp/test_memory_in_parameters.sol#L14-L21):
	- [MemoryInParameters.good(uint256[],uint256[],uint256[]).c](solidity/tmp/test_memory_in_parameters.sol#L17)
	- [MemoryInParameters.good(uint256[],uint256[],uint256[]).b](solidity/tmp/test_memory_in_parameters.sol#L16)
	- [MemoryInParameters.good(uint256[],uint256[],uint256[]).a](solidity/tmp/test_memory_in_parameters.sol#L15)


### recommendation

Check if the lengths of the array parameters are equal before use.


### locations
- solidity/tmp/test_memory_in_parameters.sol#L5-L12
- solidity/tmp/test_memory_in_parameters.sol#L14-L21

### severity
Low

### category
unchecked-array-length

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `2` instances of this issue:**

- Setter function [MemoryInParameters.bad(uint256[],uint256[],uint256[])](solidity/tmp/test_memory_in_parameters.sol#L5-L12) does not emit an event

- Setter function [MemoryInParameters.good(uint256[],uint256[],uint256[])](solidity/tmp/test_memory_in_parameters.sol#L14-L21) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/test_memory_in_parameters.sol#L5-L12
- solidity/tmp/test_memory_in_parameters.sol#L14-L21

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

## [Optimization] Use `calldata` instead of `memory` for function parameters

### description

On external functions, when using the `memory` keyword with a function argument, what's happening is a `memory` acts as an intermediate.

When the function gets called externally, the array values are kept in `calldata` and copied to memory during ABI decoding (using the opcode `calldataload` and `mstore`). 
And during the for loop, the values in the array are accessed in memory using a `mload`. That is inefficient. Reading directly from `calldata` using `calldataload` instead of going via `memory` saves the gas from the intermediate memory operations that carry the values.

More detail see [this](https://ethereum.stackexchange.com/questions/74442/when-should-i-use-calldata-and-when-should-i-use-memory)


**There is `1` instance of this issue:**

- [MemoryInParameters.bad(uint256[],uint256[],uint256[])](solidity/tmp/test_memory_in_parameters.sol#L5-L12) read-only `memory` parameters below should be changed to `calldata` :
	- [MemoryInParameters.bad(uint256[],uint256[],uint256[]).a](solidity/tmp/test_memory_in_parameters.sol#L6)


### recommendation
Use `calldata` instead of `memory` for external functions where the function argument is read-only.

### locations
- solidity/tmp/test_memory_in_parameters.sol#L5-L12

### severity
Optimization

### category
memory-in-parameters

### confidence
High
