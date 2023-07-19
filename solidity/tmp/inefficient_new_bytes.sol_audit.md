## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Expression `""` is cheaper than `new bytes(0)` | 2 |



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

## [Optimization] Expression `""` is cheaper than `new bytes(0)`

### description:




**There are `2` instances of this issue:**

- Should use `""` instead of `new bytes(0)` on [a = new bytes(0)](solidity/inefficient_new_bytes.sol#L5)

- Should use `""` instead of `new bytes(0)` on [byt = new bytes(0)](solidity/inefficient_new_bytes.sol#L6)


### recommendation:

Using empty string `""` instead of `new bytes(0)`.


### locations:
- solidity/inefficient_new_bytes.sol#L5
- solidity/inefficient_new_bytes.sol#L6

### severity:
Optimization

### category:
inefficient-new-bytes
