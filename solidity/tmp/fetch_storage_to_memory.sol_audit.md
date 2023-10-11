## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Integer Overflow and Underflow | 1 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Missing Event Setter | 4 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Using `storage` instead of `memory` for structs/arrays saves gas | 4 |
| [G-1] | Remove unused parameter variables | 2 |
| [G-2] | Dead-code: functions not used should be removed to save deployment gas | 1 |
| [G-3] | Use `assembly` to write address storage values | 2 |
| [G-4] | Use `delete` to Clear Variables | 2 |



## [Medium] Integer Overflow and Underflow

### description

    若不使用OpenZeppelin的SafeMath(或类似的库)检查溢出/下溢，
    如果用户/攻击者能够控制这种算术运算的整数操作数，
    可能会导致漏洞或意外行为。
    Solc v0.8.0为所有算术运算引入了默认的溢出/底溢检查。(见这里和这里)

**There is `1` instance of this issue:**

- externalView(uint256) has possible integer overflow/underflow:
	- [abc + tmpSt.a](solidity/tmp/fetch_storage_to_memory.sol#L29)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/tmp/fetch_storage_to_memory.sol#L29

### severity
Medium

### category
integer-overflow

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `4` instances of this issue:**

- Setter function [StorageMemory.bad(uint256)](solidity/tmp/fetch_storage_to_memory.sol#L13-L25) does not emit an event

- Setter function [StorageMemory.externalView(uint256)](solidity/tmp/fetch_storage_to_memory.sol#L27-L30) does not emit an event

- Setter function [StorageMemory.internalView(uint256)](solidity/tmp/fetch_storage_to_memory.sol#L37-L40) does not emit an event

- Setter function [StorageMemory.good(uint256)](solidity/tmp/fetch_storage_to_memory.sol#L42-L46) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/fetch_storage_to_memory.sol#L13-L25
- solidity/tmp/fetch_storage_to_memory.sol#L27-L30
- solidity/tmp/fetch_storage_to_memory.sol#L37-L40
- solidity/tmp/fetch_storage_to_memory.sol#L42-L46

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

## [Optimization] Using `storage` instead of `memory` for structs/arrays saves gas

### description
When fetching data from a storage location, assigning the data to a `memory` variable causes all fields of the struct/array to be read from storage, which incurs a Gcoldsload (**2100 gas**) for *each* field of the struct/array. If the fields are read from the new memory variable, they incur an additional `MLOAD` rather than a cheap stack read. Instead of declearing the variable with the `memory` keyword, declaring the variable with the `storage` keyword and caching any fields that need to be re-read in stack variables, will be much cheaper, only incuring the Gcoldsload for the fields actually read. The only time it makes sense to read the whole struct/array into a `memory` variable, is if the full struct/array is being returned by the function, is being passed to a function that requires `memory`, or if the array/struct is being read from another `memory` array/struct
    

**There are `4` instances of this issue:**

- local memory variable [StorageMemory.bad(uint256).tmpSt](solidity/tmp/fetch_storage_to_memory.sol#L14) is initialized from storage: [StorageMemory.userSt](solidity/tmp/fetch_storage_to_memory.sol#L11) should read data from `storage` directly

- local memory variable [StorageMemory.bad(uint256).tmpArr](solidity/tmp/fetch_storage_to_memory.sol#L18) is initialized from storage: [StorageMemory.arr](solidity/tmp/fetch_storage_to_memory.sol#L7) should read data from `storage` directly

- local memory variable [StorageMemory.externalView(uint256).tmpSt](solidity/tmp/fetch_storage_to_memory.sol#L28) is initialized from storage: [StorageMemory.userSt](solidity/tmp/fetch_storage_to_memory.sol#L11) should read data from `storage` directly

- local memory variable [StorageMemory.internalView(uint256).tmpSt](solidity/tmp/fetch_storage_to_memory.sol#L38) is initialized from storage: [StorageMemory.userSt](solidity/tmp/fetch_storage_to_memory.sol#L11) should read data from `storage` directly


### recommendation
Fetching data from `storage` directly, don't convert `storage` to `memory`

### locations
- solidity/tmp/fetch_storage_to_memory.sol#L14
- solidity/tmp/fetch_storage_to_memory.sol#L18
- solidity/tmp/fetch_storage_to_memory.sol#L28
- solidity/tmp/fetch_storage_to_memory.sol#L38

### severity
Optimization

### category
fetch-storage-to-memory

### confidence
High

## [Optimization] Remove unused parameter variables

### description

Unused parameters variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 



**There are `2` instances of this issue:**

- The param variables in [StorageMemory.bad(uint256)](solidity/tmp/fetch_storage_to_memory.sol#L13-L25) are unused.
	- [StorageMemory.bad(uint256).testInt](solidity/tmp/fetch_storage_to_memory.sol#L13)

- The param variables in [StorageMemory.good(uint256)](solidity/tmp/fetch_storage_to_memory.sol#L42-L46) are unused.
	- [StorageMemory.good(uint256).testInt](solidity/tmp/fetch_storage_to_memory.sol#L42)


### recommendation

Remove the unused parameter variables.


### locations
- solidity/tmp/fetch_storage_to_memory.sol#L13-L25
- solidity/tmp/fetch_storage_to_memory.sol#L42-L46

### severity
Optimization

### category
unused-parameter

### confidence
High

## [Optimization] Dead-code: functions not used should be removed to save deployment gas

### description
Functions that are not sued.

**There is `1` instance of this issue:**

- [StorageMemory.internalView(uint256)](solidity/tmp/fetch_storage_to_memory.sol#L37-L40) is never used and should be removed


### recommendation
Remove unused functions.

### locations
- solidity/tmp/fetch_storage_to_memory.sol#L37-L40

### severity
Optimization

### category
dead-code

### confidence
High

## [Optimization] Use `assembly` to write address storage values

### description

Where it does not affect readability, 
using assembly for simple setters allows to save gas not only on deployment, 
but also on function calls.


**There are `2` instances of this issue:**

- [tmpAddress = testAddress](solidity/tmp/fetch_storage_to_memory.sol#L22) should use `assembly` update address to save gas.

- [testAddress = tmpAddress](solidity/tmp/fetch_storage_to_memory.sol#L24) should use `assembly` update address to save gas.


### recommendation

Using `assembly` update address to save gas.

For example:
```
contract Contract1 {
    address owner;

    function assemblyUpdateOwner(address newOwner) public {
        assembly {
            sstore(owner.slot, newOwner)
        }
    }
}
```


### locations
- solidity/tmp/fetch_storage_to_memory.sol#L22
- solidity/tmp/fetch_storage_to_memory.sol#L24

### severity
Optimization

### category
assembly-update-address

### confidence
High

## [Optimization] Use `delete` to Clear Variables

### description

delete a assigns the initial value for the type to a. i.e. 
for integers it is equivalent to a = 0, but it can also be used on arrays, 
where it assigns a dynamic array of length zero or a static array of the same 
length with all elements reset. For structs, it assigns a struct with all members reset. 
Similarly, it can also be used to set an address to zero address. 
It has no effect on whole mappings though (as the keys of mappings may be arbitrary 
and are generally unknown). However, individual keys and what they map to can be deleted: 
If a is a mapping, then delete a[x] will delete the value stored at x.

The delete key better conveys the intention and is also more idiomatic. 
Consider replacing assignments of zero with delete statements.


**There are `2` instances of this issue:**

- Should use `delete` statement instead of [tmpAddress = address(0)](solidity/tmp/fetch_storage_to_memory.sol#L23)

- Should use `delete` statement instead of [arr[0] = 0](solidity/tmp/fetch_storage_to_memory.sol#L45)


### recommendation

Replacing assignments of zero with delete statements.



### locations
- solidity/tmp/fetch_storage_to_memory.sol#L23
- solidity/tmp/fetch_storage_to_memory.sol#L45

### severity
Optimization

### category
use-delete-statement

### confidence
High
