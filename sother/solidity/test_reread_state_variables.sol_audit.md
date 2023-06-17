## Summary 

### Medium Risk Issues

| |Issue|Instances|
|---|:---|:---:|
| [M-0] | Write after write | 1 |


### Gas Optimizations

| |Issue|Instances|
|---|:---|:---:|
| [G-0] | State variables should be cached in stack variables rather than re-reading them from storage | 2 |



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

- [a = stateUint256 + 1](solidity/test_reread_state_variables.sol#L9) ; [b = stateUint256 + x](solidity/test_reread_state_variables.sol#L10) ;  more than once read data from [RereadStateVariables.stateUint256](solidity/test_reread_state_variables.sol#L4) should cache the state in local memory-based variable
- [a = stateUint256 + x](solidity/test_reread_state_variables.sol#L15) ; [StateEvent(stateUint256,a)](solidity/test_reread_state_variables.sol#L16) ;  more than once read data from [RereadStateVariables.stateUint256](solidity/test_reread_state_variables.sol#L4) should cache the state in local memory-based variable

### recommendation:

Cache storage-based state variables in local memory-based variables appropriately to convert SLOADs to MLOADs and reduce gas consumption from 100 units to 3 units. than once for a function


### location:
- solidity/test_reread_state_variables.sol#L9
- solidity/test_reread_state_variables.sol#L15

### severity:
Optimization

### category:
reread-state-variables
