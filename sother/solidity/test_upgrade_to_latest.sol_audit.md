## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Conformance to Solidity naming conventions | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | use custom errors instead of revert strings | 2 |



## [Informational] Incorrect versions of Solidity

### description:

`solc` frequently releases new compiler versions. Using an old version prevents access to new Solidity security checks.
We also recommend avoiding complex `pragma` statement.

**There is `1` instance of this issue:**

- Pragma version[>=0.6.2<=0.8.19](solidity/test_upgrade_to_latest.sol#L3) is too complex


### recommendation:

Deploy with any of the following Solidity versions:
- 0.8.19

The recommendations take into account:
- Risks related to recent releases
- Risks of complex code generation changes
- Risks of new language features
- Risks of known bugs

Use a simple pragma version that allows any of these versions.
Consider using the latest version of Solidity for testing.

### location:
- solidity/test_upgrade_to_latest.sol#L3

### severity:
Informational

### category:
solc-version

## [Informational] Conformance to Solidity naming conventions

### description:

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There is `1` instance of this issue:**

- Function [SafeAdd.add_v2(uint256,uint256)](solidity/test_upgrade_to_latest.sol#L9-L11) is not in mixedCase


### recommendation:
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### location:
- solidity/test_upgrade_to_latest.sol#L9-L11

### severity:
Informational

### category:
naming-convention

## [Optimization] use custom errors instead of revert strings

### description:

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `2` instances of this issue:**

- [require(bool)((z = x + y) >= x)](solidity/test_upgrade_to_latest.sol#L10) should use custom error to save gas.

- [require(bool)((z = x + y) >= x)](solidity/test_upgrade_to_latest.sol#L7) should use custom error to save gas.


### recommendation:

Using custom errors replace `require` or `assert`.


### location:
- solidity/test_upgrade_to_latest.sol#L10
- solidity/test_upgrade_to_latest.sol#L7

### severity:
Optimization

### category:
use-custom-error
