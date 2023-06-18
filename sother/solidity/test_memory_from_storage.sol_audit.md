## Summary 

### High Risk Issues

| |Issue|Instances|
|---|:---|:---:|
| [H-0] | Uninitialized state variables | 1 |


### Gas Optimizations

| |Issue|Instances|
|---|:---|:---:|
| [G-0] | Using `storage` instead of `memory` for structs/arrays saves gas | 2 |
| [G-1] | Using `storage` instead of `memory` for structs/arrays saves gas | 2 |



## [High] Uninitialized state variables

### description:
Uninitialized state variables.

**There is `1` instance of this issue:**

- [StorageMemory.data](solidity/test_memory_from_storage.sol#L7) is never initialized. It is used in:
	- [StorageMemory.bad()](solidity/test_memory_from_storage.sol#L11-L14)
	- [StorageMemory.good()](solidity/test_memory_from_storage.sol#L22-L25)

#### Exploit scenario

```solidity
contract Uninitialized{
    address destination;

    function transfer() payable public{
        destination.transfer(msg.value);
    }
}
```
Bob calls `transfer`. As a result, the Ether are sent to the address `0x0` and are lost.


### recommendation:

Initialize all the variables. If a variable is meant to be initialized to zero, explicitly set it to zero to improve code readability.


### location:
- solidity/test_memory_from_storage.sol#L7

### severity:
High

### category:
uninitialized-state

## [Optimization] Using `storage` instead of `memory` for structs/arrays saves gas

### description:
When fetching data from a storage location, assigning the data to a `memory` variable causes all fields of the struct/array to be read from storage, which incurs a Gcoldsload (**2100 gas**) for *each* field of the struct/array. If the fields are read from the new memory variable, they incur an additional `MLOAD` rather than a cheap stack read. Instead of declearing the variable with the `memory` keyword, declaring the variable with the `storage` keyword and caching any fields that need to be re-read in stack variables, will be much cheaper, only incuring the Gcoldsload for the fields actually read. The only time it makes sense to read the whole struct/array into a `memory` variable, is if the full struct/array is being returned by the function, is being passed to a function that requires `memory`, or if the array/struct is being read from another `memory` array/struct
    

**There are `2` instances of this issue:**

- local memory variable [StorageMemory.bad().f](solidity/test_memory_from_storage.sol#L12) is initialized from storage: [StorageMemory.data](solidity/test_memory_from_storage.sol#L7) should read data from `storage` directly

- local memory variable [StorageMemory.badArr().arr](solidity/test_memory_from_storage.sol#L17) is initialized from storage: [StorageMemory.uintArr](solidity/test_memory_from_storage.sol#L9) should read data from `storage` directly


### recommendation:
Fetching data from `storage` directly, don't convert `storage` to `memory`

### location:
- solidity/test_memory_from_storage.sol#L12
- solidity/test_memory_from_storage.sol#L17

### severity:
Optimization

### category:
fetch-storage-to-memory

## [Optimization] Using `storage` instead of `memory` for structs/arrays saves gas

### description:

When fetching data from a storage location, assigning the data to a `memory` variable causes all fields of the struct/array to be read from storage, which incurs a Gcoldsload (**2100 gas**) for *each* field of the struct/array. If the fields are read from the new memory variable, they incur an additional `MLOAD` rather than a cheap stack read. Instead of declearing the variable with the `memory` keyword, declaring the variable with the `storage` keyword and caching any fields that need to be re-read in stack variables, will be much cheaper, only incuring the Gcoldsload for the fields actually read. The only time it makes sense to read the whole struct/array into a `memory` variable, is if the full struct/array is being returned by the function, is being passed to a function that requires `memory`, or if the array/struct is being read from another `memory` array/struct

More detail see [this.](https://gist.github.com/0xxfu/0ab3b64ba7b342fb88e243d82a763876)


**There are `2` instances of this issue:**

- [StorageMemory.badArr().arr](solidity/test_memory_from_storage.sol#L17) should used `storage` instead of `memory` to save gas.

- [StorageMemory.bad().f](solidity/test_memory_from_storage.sol#L12) should used `storage` instead of `memory` to save gas.


### recommendation:

Using `storage` replace `memory` in local variables.


### location:
- solidity/test_memory_from_storage.sol#L17
- solidity/test_memory_from_storage.sol#L12

### severity:
Optimization

### category:
memory-from-storage
