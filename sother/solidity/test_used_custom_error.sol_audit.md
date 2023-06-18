## Summary 

### Non-critical Issues

| |Issue|Instances|
|---|:---|:---:|
| [N-0] | Conformance to Solidity naming conventions | 3 |


### Gas Optimizations

| |Issue|Instances|
|---|:---|:---:|
| [G-0] | use custom errors instead of revert strings | 1 |



## [Informational] Conformance to Solidity naming conventions

### description:

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There are `3` instances of this issue:**

- Parameter [Exception.testRevert2(uint256)._i](solidity/test_used_custom_error.sol#L20) is not in mixedCase

- Parameter [Exception.testRequire(uint256)._i](solidity/test_used_custom_error.sol#L6) is not in mixedCase

- Parameter [Exception.testRevert1(uint256)._i](solidity/test_used_custom_error.sol#L11) is not in mixedCase


### recommendation:
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### location:
- solidity/test_used_custom_error.sol#L20
- solidity/test_used_custom_error.sol#L6
- solidity/test_used_custom_error.sol#L11

### severity:
Informational

### category:
naming-convention

## [Optimization] use custom errors instead of revert strings

### description:

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There is `1` instance of this issue:**

- [require(bool,string)(_i > 10,Input must be greater than 10)](solidity/test_used_custom_error.sol#L7) should use custom error to save gas.


### recommendation:

Using custom errors replace `require` or `assert`.


### location:
- solidity/test_used_custom_error.sol#L7

### severity:
Optimization

### category:
use-custom-error
