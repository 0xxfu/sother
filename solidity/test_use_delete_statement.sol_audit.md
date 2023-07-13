## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Use `uint256(1)/uint256(2)` instead for `true` and `false` boolean states | 1 |
| [G-1] | Use `delete` to Clear Variables | 8 |



## [Informational] Incorrect versions of Solidity

### description:

`solc` frequently releases new compiler versions. Using an old version prevents access to new Solidity security checks.
We also recommend avoiding complex `pragma` statement.

**There is `1` instance of this issue:**

- solc-0.8.19 is not recommended for deployment


### recommendation:

Deploy with any of the following Solidity versions:
- 0.8.20

The recommendations take into account:
- Risks related to recent releases
- Risks of complex code generation changes
- Risks of new language features
- Risks of known bugs

Use a simple pragma version that allows any of these versions.
Consider using the latest version of Solidity for testing.

### locations:
- 

### severity:
Informational

### category:
solc-version

## [Optimization] Use `uint256(1)/uint256(2)` instead for `true` and `false` boolean states

### description:

```solidity
// Booleans are more expensive than uint256 or any type that takes up a full
// word because each write operation emits an extra SLOAD to first read the
// slot's contents, replace the bits taken up by the boolean, and then write
// back. This is the compiler's defense against contract upgrades and
// pointer aliasing, and it cannot be disabled.

// The values being non-zero value makes deployment a bit more expensive,
// but in exchange the refund on every call to nonReentrant will be lower in
// amount. Since refunds are capped to a percentage of the total
// transaction's gas, it is best to keep them low in cases like this one, to
// increase the likelihood of the full refund coming into effect.
```
more detail see [this](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/58f635312aa21f947cae5f8578638a85aa2519f5/contracts/security/ReentrancyGuard.sol#L23-L33)
    
    

**There is `1` instance of this issue:**

- bool state [UseDeleteStatement.boolean](solidity/test_use_delete_statement.sol#L5) should be replaced by `uint256(1)` and `uint256(2)`

### recommendation:
Use `uint256(1)` and `uint256(2)` for true/false to avoid a Gwarmaccess (**[100 gas](https://gist.github.com/0xxfu/d12e22af63cd2e0e9d6a8550360b2959)**) for the extra SLOAD, and to avoid Gsset (**20000 gas**) when changing from `false` to `true`, after having been `true` in the past

### locations:
- solidity/test_use_delete_statement.sol#L5

### severity:
Optimization

### category:
bool-state-variables

## [Optimization] Use `delete` to Clear Variables

### description:

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


**There are `8` instances of this issue:**

- Should use `delete` statement instead of [ui256 = 0](solidity/test_use_delete_statement.sol#L8)

- Should use `delete` statement instead of [i256 = 0](solidity/test_use_delete_statement.sol#L9)

- Should use `delete` statement instead of [addr = address(0)](solidity/test_use_delete_statement.sol#L10)

- Should use `delete` statement instead of [boolean = false](solidity/test_use_delete_statement.sol#L11)

- Should use `delete` statement instead of [_ui256 = 0](solidity/test_use_delete_statement.sol#L15)

- Should use `delete` statement instead of [_i256 = 0](solidity/test_use_delete_statement.sol#L16)

- Should use `delete` statement instead of [_addr = address(0)](solidity/test_use_delete_statement.sol#L17)

- Should use `delete` statement instead of [_boolean = false](solidity/test_use_delete_statement.sol#L18)


### recommendation:

Replacing assignments of zero with delete statements.



### locations:
- solidity/test_use_delete_statement.sol#L8
- solidity/test_use_delete_statement.sol#L9
- solidity/test_use_delete_statement.sol#L10
- solidity/test_use_delete_statement.sol#L11
- solidity/test_use_delete_statement.sol#L15
- solidity/test_use_delete_statement.sol#L16
- solidity/test_use_delete_statement.sol#L17
- solidity/test_use_delete_statement.sol#L18

### severity:
Optimization

### category:
use-delete-statement
