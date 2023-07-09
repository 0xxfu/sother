## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Low-level calls | 1 |



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

## [Informational] Low-level calls

### description:
The use of low-level calls is error-prone. Low-level calls do not check for [code existence](https://solidity.readthedocs.io/en/v0.4.25/control-structures.html#error-handling-assert-require-revert-and-exceptions) or call success.

**There is `1` instance of this issue:**

- Low level call in [Address.sendValue(address,uint256)](solidity/test_reentrancy_send_value.sol#L6-L15):
	- [(success) = recipient.call{value: amount}()](solidity/test_reentrancy_send_value.sol#L11)


### recommendation:
Avoid low-level calls. Check the call success. If the call is meant for a contract, check for code existence.

### locations:
- solidity/test_reentrancy_send_value.sol#L6-L15

### severity:
Informational

### category:
low-level-calls
