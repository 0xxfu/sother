## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Write after write | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | State variables should be cached in stack variables rather than re-reading them from storage | 2 |
| [G-1] | Use indexed events for value types as they are less costly compared to non-indexed ones | 1 |



## [Medium] Write after write

### description:
Detects variables that are written but never read and written again.

**There is `1` instance of this issue:**

- [RereadStateVariables.stateUint256](solidity/test_reread_state_variables.sol#L4) is written in both
	[stateUint256 = x + 1](solidity/test_reread_state_variables.sol#L21)
	[stateUint256 = a + b](solidity/test_reread_state_variables.sol#L23)

#### Exploit scenario

    ```solidity
    contract Buggy{
        function my_func() external initializer{
            // ...
            a = b;
            a = c;
            // ..
        }
    }
    ```
    `a` is first asigned to `b`, and then to `c`. As a result the first write does nothing.

### recommendation:
Fix or remove the writes.

### location:
- solidity/test_reread_state_variables.sol#L4

### severity:
Medium

### category:
write-after-write

## [Optimization] State variables should be cached in stack variables rather than re-reading them from storage

### description:

The instances below point to the second+ access of a state variable within a function. Caching of a state variable replaces each Gwarmaccess (**100 gas**) with a much cheaper stack read. Other less obvious fixes/optimizations include having local memory caches of state variable structs, or having local caches of state variable contracts/addresses.

More detail see [this.](https://gist.github.com/0xxfu/af8f63ccbf36af9d067ed6eff9ff7129)


**There are `2` instances of this issue:**

- [RereadStateVariables.stateUint256](solidity/test_reread_state_variables.sol#L4) should be cached with local memory-based variable in [RereadStateVariables.bad2(uint256)](solidity/test_reread_state_variables.sol#L14-L17), It is called more than once:
	- [a = stateUint256 + x](solidity/test_reread_state_variables.sol#L15)
	- [StateEvent(stateUint256,a)](solidity/test_reread_state_variables.sol#L16)

- [RereadStateVariables.stateUint256](solidity/test_reread_state_variables.sol#L4) should be cached with local memory-based variable in [RereadStateVariables.bad(uint256)](solidity/test_reread_state_variables.sol#L8-L12), It is called more than once:
	- [a = stateUint256 + 1](solidity/test_reread_state_variables.sol#L9)
	- [b = stateUint256 + x](solidity/test_reread_state_variables.sol#L10)


### recommendation:

Cache storage-based state variables in local memory-based variables appropriately to convert SLOADs to MLOADs and reduce gas consumption from 100 units to 3 units. than once for a function


### location:
- solidity/test_reread_state_variables.sol#L4
- solidity/test_reread_state_variables.sol#L4

### severity:
Optimization

### category:
reread-state-variables

## [Optimization] Use indexed events for value types as they are less costly compared to non-indexed ones

### description:

Using the `indexed` keyword for [value types](https://docs.soliditylang.org/en/v0.8.20/types.html#value-types) (`bool/int/address/string/bytes`) saves gas costs, as seen in [this example](https://gist.github.com/0xxfu/c292a65ecb61cae6fd2090366ea0877e).

However, this is only the case for value types, whereas indexing [reference types](https://docs.soliditylang.org/en/v0.8.20/types.html#reference-types) (`array/struct`) are more expensive than their unindexed version.


**There is `1` instance of this issue:**

- The following variables should be indexed in [RereadStateVariables.StateEvent(uint256,uint256)](solidity/test_reread_state_variables.sol#L6):

	- [a](solidity/test_reread_state_variables.sol#L6)

	- [state](solidity/test_reread_state_variables.sol#L6)


### recommendation:

Using the `indexed` keyword for values types `bool/int/address/string/bytes` in event


### location:
- solidity/test_reread_state_variables.sol#L6

### severity:
Optimization

### category:
unindexed-event
