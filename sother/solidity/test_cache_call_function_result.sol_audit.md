## Summary 

### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | The result of function calls should be cached rather than re-calling the function | 1 |



## [Optimization] The result of function calls should be cached rather than re-calling the function

### description:

The instances below point to the second+ call of the function within a single function


**There is `1` instance of this issue:**

- `CallFunctionResult.externalPure()` called result should be cached with local variable in [CallFunctionResult.bad(uint256)](solidity/test_cache_call_function_result.sol#L5-L10), It is called more than once:
	- [a = a + externalPure()](solidity/test_cache_call_function_result.sol#L6)
	- [a = a + externalPure()](solidity/test_cache_call_function_result.sol#L7)


### recommendation:

Using local variable to cache function called result if the same function called more than once.


### location:
- solidity/test_cache_call_function_result.sol#L5-L10

### severity:
Optimization

### category:
cache-call-function-result
