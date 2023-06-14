## Summary 

### Non-critical Issues

| |Issue|Instances|
|---|:---|:---:|
| [N-0] | Conformance to Solidity naming conventions | 3 |


### Gas Optimizations

| |Issue|Instances|
|---|:---|:---:|
| [G-0] | Using `bool` replace `uint256(1)` and `uint256(2)` for true/false | 1 |



## [Informational] Conformance to Solidity naming conventions

### description:

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There are `3` instances of this issue:**

- Function [MappingUint256s.set_2E3(uint256,uint256)](solidity/test_bool_state_variables.sol#L49-L51) is not in mixedCase

- Function [MappingUint8s.set_Hl1r(uint256,uint8)](solidity/test_bool_state_variables.sol#L32-L34) is not in mixedCase

- Function [MappingBools.set_a81(uint256,bool)](solidity/test_bool_state_variables.sol#L15-L17) is not in mixedCase


### recommendation:
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### location:
- solidity/test_bool_state_variables.sol#L49-L51
- solidity/test_bool_state_variables.sol#L32-L34
- solidity/test_bool_state_variables.sol#L15-L17

### severity:
Informational

### category:
naming-convention

## [Optimization] Using `bool` replace `uint256(1)` and `uint256(2)` for true/false

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

- bool state [MappingBools.data2](solidity/test_bool_state_variables.sol#L11) should be replaced by `uint256(1)` and `uint256(2)`

### recommendation:
Use `uint256(1)` and `uint256(2)` for true/false to avoid a Gwarmaccess (**[100 gas](https://gist.github.com/0xxfu/d12e22af63cd2e0e9d6a8550360b2959)**) for the extra SLOAD, and to avoid Gsset (**20000 gas**) when changing from `false` to `true`, after having been `true` in the past

### location:
- solidity/test_bool_state_variables.sol#L11

### severity:
Optimization

### category:
bool-state-variables
