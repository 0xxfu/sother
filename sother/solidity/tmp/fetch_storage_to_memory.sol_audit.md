## Summary 

### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Dead-code: functions not used should be removed to save deployment gas | 1 |
| [G-1] | Using `storage` instead of `memory` for structs/arrays saves gas | 3 |



## [Optimization] Dead-code: functions not used should be removed to save deployment gas

### description:
Functions that are not sued.

**There is `1` instance of this issue:**

- [StorageMemory.internalView(uint256)](solidity/fetch_storage_to_memory.sol#L37-L40) is never used and should be removed


### recommendation:
Remove unused functions.

### location:
- solidity/fetch_storage_to_memory.sol#L37-L40

### severity:
Optimization

### category:
dead-code

## [Optimization] Using `storage` instead of `memory` for structs/arrays saves gas

### description:
When fetching data from a storage location, assigning the data to a `memory` variable causes all fields of the struct/array to be read from storage, which incurs a Gcoldsload (**2100 gas**) for *each* field of the struct/array. If the fields are read from the new memory variable, they incur an additional `MLOAD` rather than a cheap stack read. Instead of declearing the variable with the `memory` keyword, declaring the variable with the `storage` keyword and caching any fields that need to be re-read in stack variables, will be much cheaper, only incuring the Gcoldsload for the fields actually read. The only time it makes sense to read the whole struct/array into a `memory` variable, is if the full struct/array is being returned by the function, is being passed to a function that requires `memory`, or if the array/struct is being read from another `memory` array/struct
    

**There are `3` instances of this issue:**

- local memory variable [StorageMemory.bad(uint256).tmpSt](solidity/fetch_storage_to_memory.sol#L14) is initialized from storage: [StorageMemory.userSt](solidity/fetch_storage_to_memory.sol#L11) should read data from `storage` directly

- local memory variable [StorageMemory.bad(uint256).tmpArr](solidity/fetch_storage_to_memory.sol#L18) is initialized from storage: [StorageMemory.arr](solidity/fetch_storage_to_memory.sol#L7) should read data from `storage` directly

- local memory variable [StorageMemory.internalView(uint256).tmpSt](solidity/fetch_storage_to_memory.sol#L38) is initialized from storage: [StorageMemory.userSt](solidity/fetch_storage_to_memory.sol#L11) should read data from `storage` directly


### recommendation:
Fetching data from `storage` directly, don't convert `storage` to `memory`

### location:
- solidity/fetch_storage_to_memory.sol#L14
- solidity/fetch_storage_to_memory.sol#L18
- solidity/fetch_storage_to_memory.sol#L38

### severity:
Optimization

### category:
fetch-storage-to-memory
