## Summary 

### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Dead-code: functions not used should be removed to save deployment gas | 1 |



## [Optimization] Dead-code: functions not used should be removed to save deployment gas

### description:
Functions that are not sued.

**There is `1` instance of this issue:**

- [UnusedInternalFunction.bad(uint256)](solidity/test_unused_internal_function.sol#L6-L8) is never used and should be removed


### recommendation:
Remove unused functions.

### location:
- solidity/test_unused_internal_function.sol#L6-L8

### severity:
Optimization

### category:
dead-code
