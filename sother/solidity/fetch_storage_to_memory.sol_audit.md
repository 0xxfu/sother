## Summary 

### Non-critical Issues

| |Issue|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 2 |


### Gas Optimizations

| |Issue|Instances|
|---|:---|:---:|
| [G-0] | Using `storage` instead of `memory` for structs/arrays saves gas | 2 |



## [Informational] Incorrect versions of Solidity

### description:

`solc` frequently releases new compiler versions. Using an old version prevents access to new Solidity security checks.
We also recommend avoiding complex `pragma` statement.

**There are `2` instances of this issue:**

- solc-0.8.19 is not recommended for deployment

- Pragma version[0.8.19](solidity/fetch_storage_to_memory.sol#L2) necessitates a version too recent to be trusted. Consider deploying with 0.8.18.


### recommendation:

Deploy with any of the following Solidity versions:
- 0.8.18

The recommendations take into account:
- Risks related to recent releases
- Risks of complex code generation changes
- Risks of new language features
- Risks of known bugs

Use a simple pragma version that allows any of these versions.
Consider using the latest version of Solidity for testing.

### location:
- 
- solidity/fetch_storage_to_memory.sol#L2

### severity:
Informational

### category:
solc-version

## [Optimization] Using `storage` instead of `memory` for structs/arrays saves gas

### description:
When fetching data from a storage location, assigning the data to a `memory` variable causes all fields of the struct/array to be read from storage, which incurs a Gcoldsload (**2100 gas**) for *each* field of the struct/array. If the fields are read from the new memory variable, they incur an additional `MLOAD` rather than a cheap stack read. Instead of declearing the variable with the `memory` keyword, declaring the variable with the `storage` keyword and caching any fields that need to be re-read in stack variables, will be much cheaper, only incuring the Gcoldsload for the fields actually read. The only time it makes sense to read the whole struct/array into a `memory` variable, is if the full struct/array is being returned by the function, is being passed to a function that requires `memory`, or if the array/struct is being read from another `memory` array/struct
    

**There are `2` instances of this issue:**

- local memory variable [StorageMemory.bad(uint256).tmpSt](solidity/fetch_storage_to_memory.sol#L15) is initialized from storage: [StorageMemory.userSt](solidity/fetch_storage_to_memory.sol#L12)

- local memory variable [StorageMemory.bad(uint256).tmpArr](solidity/fetch_storage_to_memory.sol#L19) is initialized from storage: [StorageMemory.arr](solidity/fetch_storage_to_memory.sol#L8)


### recommendation:
Fetching data from `storage` directly, don't convert `storage` to `memory`

### location:
- solidity/fetch_storage_to_memory.sol#L15
- solidity/fetch_storage_to_memory.sol#L19

### severity:
Optimization

### category:
fetch-storage-to-memory
