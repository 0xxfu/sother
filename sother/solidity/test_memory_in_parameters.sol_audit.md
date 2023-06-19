## Summary 

### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Use `calldata` instead of `memory` for function parameters | 1 |



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

### location:
- solidity/test_memory_in_parameters.sol#L5-L12

### severity:
Optimization

### category:
memory-in-parameters
