## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Shortening revert strings to fit in 32 `bytes` | 2 |



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

## [Optimization] Shortening revert strings to fit in 32 `bytes`

### description:

In Solidity, the size of a string is not fixed and depends on the length of the string. 
Each character in a string requires 2 `bytes` of storage. 
Additionally, there is an overhead of 32 `bytes` to store the length of the string.

Shortening revert strings to fit in 32 bytes will decrease deployment time gas 
and will decrease runtime gas when the revert condition is met.


**There are `2` instances of this issue:**

- `revert(string)(long long long long long)` (solidity/test_revert_long_strings.sol#L6) should be shortened strings to fit in 32 `bytes` (16 characters).

- `require(bool,string)(a != 0,long long long long long)` (solidity/test_revert_long_strings.sol#L11) should be shortened strings to fit in 32 `bytes` (16 characters).


### recommendation:

Shortening revert strings to fit in 32 `bytes`


### locations:
- solidity/test_revert_long_strings.sol#L6
- solidity/test_revert_long_strings.sol#L11

### severity:
Optimization

### category:
revert-long-strings
