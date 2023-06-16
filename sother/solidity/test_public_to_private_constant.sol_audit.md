## Summary 

### Non-critical Issues

| |Issue|Instances|
|---|:---|:---:|
| [N-0] | Conformance to Solidity naming conventions | 3 |


### Gas Optimizations

| |Issue|Instances|
|---|:---|:---:|
| [G-0] | Using `private` rather than `public` for constants, saves gas | 3 |



## [Informational] Conformance to Solidity naming conventions

### description:

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There are `3` instances of this issue:**

- Constant [PublicToPrivateConstant.priUint256](solidity/test_public_to_private_constant.sol#L7) is not in UPPER_CASE_WITH_UNDERSCORES

- Constant [PublicToPrivateConstant.priAddress](solidity/test_public_to_private_constant.sol#L8) is not in UPPER_CASE_WITH_UNDERSCORES

- Constant [PublicToPrivateConstant.priBytes](solidity/test_public_to_private_constant.sol#L9) is not in UPPER_CASE_WITH_UNDERSCORES


### recommendation:
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### location:
- solidity/test_public_to_private_constant.sol#L7
- solidity/test_public_to_private_constant.sol#L8
- solidity/test_public_to_private_constant.sol#L9

### severity:
Informational

### category:
naming-convention

## [Optimization] Using `private` rather than `public` for constants, saves gas

### description:

If needed, the values can be read from the verified contract source code, or if there are multiple values there can be a single getter function that [returns a tuple](https://github.com/code-423n4/2022-08-frax/blob/90f55a9ce4e25bceed3a74290b854341d8de6afa/src/contracts/FraxlendPair.sol#L156-L178) of the values of all currently-public constants. 

Saves **3406-3606 gas** in deployment gas due to the compiler not having to create non-payable getter functions for deployment calldata, not having to store the bytes of the value outside of where it's used, and not adding another entry to the method ID table


**There are `3` instances of this issue:**

- [PublicToPrivateConstant.pAddress](solidity/test_public_to_private_constant.sol#L5) should be used `private` visibility to save gas.

- [PublicToPrivateConstant.pUint256](solidity/test_public_to_private_constant.sol#L4) should be used `private` visibility to save gas.

- [PublicToPrivateConstant.pBytes](solidity/test_public_to_private_constant.sol#L6) should be used `private` visibility to save gas.


### recommendation:

Using `private` replace `public` with constant.


### location:
- solidity/test_public_to_private_constant.sol#L5
- solidity/test_public_to_private_constant.sol#L4
- solidity/test_public_to_private_constant.sol#L6

### severity:
Optimization

### category:
public-to-private-constant
