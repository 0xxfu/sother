## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 2 |
| [N-1] | Conformance to Solidity naming conventions | 1 |
| [N-2] | .. | 2 |
| [N-3] | Unnecessary Public Function Modifier | 2 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Should use latest solidity version `0.8.21` for gas reduction and improved security. | 1 |
| [G-1] | Using custom errors replace `require` or `assert` | 2 |



## [Informational] Incorrect versions of Solidity

### description

`solc` frequently releases new compiler versions. Using an old version prevents access to new Solidity security checks.
We also recommend avoiding complex `pragma` statement.

**There are `2` instances of this issue:**

- Pragma version[>=0.6.2<=0.8.17](solidity/tmp/test_upgrade_to_latest.sol#L3) is too complex

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
- solidity/tmp/test_upgrade_to_latest.sol#L3
- 

### severity
Informational

### category
solc-version

### confidence
High

## [Informational] Conformance to Solidity naming conventions

### description

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There is `1` instance of this issue:**

- Function [SafeAdd.add_v2(uint256,uint256)](solidity/tmp/test_upgrade_to_latest.sol#L9-L11) is not in mixedCase


### recommendation
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations
- solidity/tmp/test_upgrade_to_latest.sol#L9-L11

### severity
Informational

### category
naming-convention

### confidence
High

## [Informational] ..

### description
..

**There are `2` instances of this issue:**

- require() missing error messages
	 - [require(bool)((z = x + y) >= x)](solidity/tmp/test_upgrade_to_latest.sol#L7)

- require() missing error messages
	 - [require(bool)((z = x + y) >= x)](solidity/tmp/test_upgrade_to_latest.sol#L10)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/tmp/test_upgrade_to_latest.sol#L7
- solidity/tmp/test_upgrade_to_latest.sol#L10

### severity
Informational

### category
error-msg

### confidence
Medium

## [Informational] Unnecessary Public Function Modifier

### description
Detect the public function which can be replaced with external

**There are `2` instances of this issue:**

- function:[SafeAdd.add(uint256,uint256)](solidity/tmp/test_upgrade_to_latest.sol#L6-L8)is public and can be replaced with external 

- function:[SafeAdd.add_v2(uint256,uint256)](solidity/tmp/test_upgrade_to_latest.sol#L9-L11)is public and can be replaced with external 

#### Exploit scenario

```solidity
contract A{}
contract B is A{
    constructor() public A(){}
}
```
When reading `B`'s constructor definition, we might assume that `A()` initiates the contract, but no code is executed.

### recommendation
Replace public with external

### locations
- solidity/tmp/test_upgrade_to_latest.sol#L6-L8
- solidity/tmp/test_upgrade_to_latest.sol#L9-L11

### severity
Informational

### category
unnecessary-public-function-modifier

### confidence
High

## [Optimization] Should use latest solidity version `0.8.21` for gas reduction and improved security.

### description

[Solidity `0.8.21`](https://soliditylang.org/blog/2023/07/19/solidity-0.8.21-release-announcement) has many optimization with compiler and bugfixes, 
please upgrade Solidity to the latest version(`0.8.21`) for gas reduction and improved security.


**There is `1` instance of this issue:**

- pragma solidity version [>=0.6.2<=0.8.17](solidity/tmp/test_upgrade_to_latest.sol#L3) should upgrade to the latest version: 0.8.21

### recommendation
Upgrade solidity version to the latest version: 0.8.21

### locations
- solidity/tmp/test_upgrade_to_latest.sol#L3

### severity
Optimization

### category
upgrade-to-latest

### confidence
High

## [Optimization] Using custom errors replace `require` or `assert`

### description

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `2` instances of this issue:**

- [require(bool)((z = x + y) >= x)](solidity/tmp/test_upgrade_to_latest.sol#L7) should use custom error to save gas.

- [require(bool)((z = x + y) >= x)](solidity/tmp/test_upgrade_to_latest.sol#L10) should use custom error to save gas.


### recommendation

Using custom errors replace `require` or `assert`.


### locations
- solidity/tmp/test_upgrade_to_latest.sol#L7
- solidity/tmp/test_upgrade_to_latest.sol#L10

### severity
Optimization

### category
use-custom-error

### confidence
High
