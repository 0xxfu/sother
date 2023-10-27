## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | .. | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Using custom errors replace `require` or `assert` | 2 |



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

## [Informational] ..

### description
..

**There is `1` instance of this issue:**

- require() missing error messages
	 - [require(bool)(a > 100)](solidity/test_missing_msg_in_require.sol#L3)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/test_missing_msg_in_require.sol#L3

### severity
Informational

### category
error-msg

### confidence
Medium

## [Optimization] Using custom errors replace `require` or `assert`

### description

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `2` instances of this issue:**

- [require(bool)(a > 100)](solidity/test_missing_msg_in_require.sol#L3) should use custom error to save gas.

- [require(bool,string)(a > 1000,"cannot < 100")](solidity/test_missing_msg_in_require.sol#L7) should use custom error to save gas.


### recommendation

Using custom errors replace `require` or `assert`.


### locations
- solidity/test_missing_msg_in_require.sol#L3
- solidity/test_missing_msg_in_require.sol#L7

### severity
Optimization

### category
use-custom-error

### confidence
High
