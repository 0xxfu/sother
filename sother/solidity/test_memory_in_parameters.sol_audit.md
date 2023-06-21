## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Missing array length equality checks may lead to incorrect or undefined behavior | 2 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Use `calldata` instead of `memory` for function parameters | 1 |



## [Low] Missing array length equality checks may lead to incorrect or undefined behavior

### description:

If the length of the arrays are not required to be of the same length, user operations may not be fully executed due to a mismatch in the number of items iterated over, versus the number of items provided in the second array


**There are `2` instances of this issue:**

- Missing check lengths of parameters below in function [MemoryInParameters.bad(uint256[],uint256[],uint256[])](solidity/test_memory_in_parameters.sol#L5-L12):
	- [MemoryInParameters.bad(uint256[],uint256[],uint256[]).a](solidity/test_memory_in_parameters.sol#L6)
	- [MemoryInParameters.bad(uint256[],uint256[],uint256[]).b](solidity/test_memory_in_parameters.sol#L7)
	- [MemoryInParameters.bad(uint256[],uint256[],uint256[]).c](solidity/test_memory_in_parameters.sol#L8)

- Missing check lengths of parameters below in function [MemoryInParameters.good(uint256[],uint256[],uint256[])](solidity/test_memory_in_parameters.sol#L14-L21):
	- [MemoryInParameters.good(uint256[],uint256[],uint256[]).c](solidity/test_memory_in_parameters.sol#L17)
	- [MemoryInParameters.good(uint256[],uint256[],uint256[]).b](solidity/test_memory_in_parameters.sol#L16)
	- [MemoryInParameters.good(uint256[],uint256[],uint256[]).a](solidity/test_memory_in_parameters.sol#L15)


### recommendation:

Check if the lengths of the array parameters are equal before use.


### locations:
- solidity/test_memory_in_parameters.sol#L5-L12
- solidity/test_memory_in_parameters.sol#L14-L21

### severity:
Low

### category:
unchecked-array-length

## [Optimization] Use `calldata` instead of `memory` for function parameters

### description:

On external functions, when using the `memory` keyword with a function argument, what's happening is a `memory` acts as an intermediate.

When the function gets called externally, the array values are kept in `calldata` and copied to memory during ABI decoding (using the opcode `calldataload` and `mstore`). 
And during the for loop, the values in the array are accessed in memory using a `mload`. That is inefficient. Reading directly from `calldata` using `calldataload` instead of going via `memory` saves the gas from the intermediate memory operations that carry the values.

More detail see [this](https://ethereum.stackexchange.com/questions/74442/when-should-i-use-calldata-and-when-should-i-use-memory)


**There is `1` instance of this issue:**

- [MemoryInParameters.bad(uint256[],uint256[],uint256[])](solidity/test_memory_in_parameters.sol#L5-L12) read-only `memory` parameters below should be changed to `calldata` :
	- [MemoryInParameters.bad(uint256[],uint256[],uint256[]).a](solidity/test_memory_in_parameters.sol#L6)


### recommendation:
Use `calldata` instead of `memory` for external functions where the function argument is read-only.

### locations:
- solidity/test_memory_in_parameters.sol#L5-L12

### severity:
Optimization

### category:
memory-in-parameters
