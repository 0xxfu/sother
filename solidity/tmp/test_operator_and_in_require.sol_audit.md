## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Unnecessary Public Function Modifier | 2 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Using custom errors replace `require` or `assert` | 3 |
| [G-1] | Splitting `&&` in `require()` statements to saves gas | 1 |



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

## [Informational] Unnecessary Public Function Modifier

### description
Detect the public function which can be replaced with external

**There are `2` instances of this issue:**

- function:[SplittingRequire.requireSplit(uint256)](solidity/tmp/test_operator_and_in_require.sol#L6-L14)is public and can be replaced with external 

- function:[SplittingRequire.requireAnd(uint256)](solidity/tmp/test_operator_and_in_require.sol#L16-L22)is public and can be replaced with external 

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
- solidity/tmp/test_operator_and_in_require.sol#L6-L14
- solidity/tmp/test_operator_and_in_require.sol#L16-L22

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


**There are `3` instances of this issue:**

- [require(bool,string)(a >= 100,"err")](solidity/tmp/test_operator_and_in_require.sol#L8) should use custom error to save gas.

- [require(bool,string)(a <= 1000,"err")](solidity/tmp/test_operator_and_in_require.sol#L10) should use custom error to save gas.

- [require(bool,string)(a >= 100 && a <= 1000,"err")](solidity/tmp/test_operator_and_in_require.sol#L18) should use custom error to save gas.


### recommendation

Using custom errors replace `require` or `assert`.


### locations
- solidity/tmp/test_operator_and_in_require.sol#L8
- solidity/tmp/test_operator_and_in_require.sol#L10
- solidity/tmp/test_operator_and_in_require.sol#L18

### severity
Optimization

### category
use-custom-error

### confidence
High

## [Optimization] Splitting `&&` in `require()` statements to saves gas

### description

Instead of using the `&&` operator in a single require statement to check multiple conditions,using multiple require statements with 1 condition per require statement will save 3 GAS per `&&`

More detail see [this.](https://gist.github.com/0xxfu/478b64036c4cdc45d3d278cd5bd8eb9b)


**There is `1` instance of this issue:**

- [require(bool,string)(a >= 100 && a <= 1000,"err")](solidity/tmp/test_operator_and_in_require.sol#L18) contain `&&` operator should be split into multiple `require()` statements.


### recommendation

Splitting `&&` operator in `require()` into multiple `require()` statements.

```
// Before
require(result >= a && result <= b);

// After
require(result >= a);
require(result <= b);
```


### locations
- solidity/tmp/test_operator_and_in_require.sol#L18

### severity
Optimization

### category
operator-and-in-require

### confidence
High
