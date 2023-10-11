## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | `revert CustomError()` should be used instead of `assert()` | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Conformance to Solidity naming conventions | 3 |
| [N-2] | Unnecessary Public Function Modifier | 4 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Using custom errors replace `require` or `assert` | 2 |



## [Low] `revert CustomError()` should be used instead of `assert()`

### description

Prior to solidity version 0.8.0, hitting an assert consumes the **remainder of the 
transaction's available gas** rather than returning it, as `require()`/`revert()` do. 
`assert()` should be avoided even past solidity version 0.8.0 as its 
[documentation](https://docs.soliditylang.org/en/latest/control-structures.html#panic-via-assert-and-error-via-require) 
states that "The assert function creates an error of type Panic(uint256). ... 
Properly functioning code should never create a Panic, not even on invalid external 
input. If this happens, then there is a bug in your contract which you should fix.



**There is `1` instance of this issue:**

- [assert(bool)(a <= 10)](solidity/tmp/test_deprecated_assert.sol#L26) should be replaced by `if (!condition) revert CustomError();`.


### recommendation

Please use `if (!condition) revert CustomError();` instead of `assert()`.


### locations
- solidity/tmp/test_deprecated_assert.sol#L26

### severity
Low

### category
deprecated-assert

### confidence
High

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

## [Informational] Conformance to Solidity naming conventions

### description

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There are `3` instances of this issue:**

- Parameter [DeprecatedAssert.testRequire(uint256)._i](solidity/tmp/test_deprecated_assert.sol#L5) is not in mixedCase

- Parameter [DeprecatedAssert.testRevert1(uint256)._i](solidity/tmp/test_deprecated_assert.sol#L10) is not in mixedCase

- Parameter [DeprecatedAssert.testRevert2(uint256)._i](solidity/tmp/test_deprecated_assert.sol#L19) is not in mixedCase


### recommendation
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations
- solidity/tmp/test_deprecated_assert.sol#L5
- solidity/tmp/test_deprecated_assert.sol#L10
- solidity/tmp/test_deprecated_assert.sol#L19

### severity
Informational

### category
naming-convention

### confidence
High

## [Informational] Unnecessary Public Function Modifier

### description
Detect the public function which can be replaced with external

**There are `4` instances of this issue:**

- function:[DeprecatedAssert.testRequire(uint256)](solidity/tmp/test_deprecated_assert.sol#L5-L7)is public and can be replaced with external 

- function:[DeprecatedAssert.testRevert1(uint256)](solidity/tmp/test_deprecated_assert.sol#L10-L14)is public and can be replaced with external 

- function:[DeprecatedAssert.testRevert2(uint256)](solidity/tmp/test_deprecated_assert.sol#L19-L23)is public and can be replaced with external 

- function:[DeprecatedAssert.testAssert(uint256)](solidity/tmp/test_deprecated_assert.sol#L25-L27)is public and can be replaced with external 

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
- solidity/tmp/test_deprecated_assert.sol#L5-L7
- solidity/tmp/test_deprecated_assert.sol#L10-L14
- solidity/tmp/test_deprecated_assert.sol#L19-L23
- solidity/tmp/test_deprecated_assert.sol#L25-L27

### severity
Informational

### category
unnecessary-public-function-modifier

### confidence
High

## [Optimization] Using custom errors replace `require` or `assert`

### description

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `2` instances of this issue:**

- [require(bool,string)(_i > 10,"Input must be greater than 10")](solidity/tmp/test_deprecated_assert.sol#L6) should use custom error to save gas.

- [assert(bool)(a <= 10)](solidity/tmp/test_deprecated_assert.sol#L26) should use custom error to save gas.


### recommendation

Using custom errors replace `require` or `assert`.


### locations
- solidity/tmp/test_deprecated_assert.sol#L6
- solidity/tmp/test_deprecated_assert.sol#L26

### severity
Optimization

### category
use-custom-error

### confidence
High
