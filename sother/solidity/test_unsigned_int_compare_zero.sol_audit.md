## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | `++i` costs less gas than `i++`, especially when it's used in for-loops (`--i/i--` too) | 3 |



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

## [Optimization] `++i` costs less gas than `i++`, especially when it's used in for-loops (`--i/i--` too)

### description:

`!= 0` costs less gas compared to `> 0` for unsigned integers in require statements 
with the optimizer enabled (6 gas)

While it may seem that `> 0` is cheaper than `!=`, this is only true without the 
optimizer enabled and outside a require statement. 
If you enable the optimizer at 10k and you’re in a `require` statement, 
this will save gas.



**There are `3` instances of this issue:**

- `a > 0` (solidity/test_unsigned_int_compare_zero.sol#L3) should use `!= 0` instead of `> 0` for unsigned integer comparison.

- `require(bool,string)(a > 0,err)` (solidity/test_unsigned_int_compare_zero.sol#L9) should use `!= 0` instead of `> 0` for unsigned integer comparison.

- `require(bool,string)(a > 0,err)` (solidity/test_unsigned_int_compare_zero.sol#L13) should use `!= 0` instead of `> 0` for unsigned integer comparison.


### recommendation:

Use `!= 0` instead of `> 0` for unsigned integer comparison.


### locations:
- solidity/test_unsigned_int_compare_zero.sol#L3
- solidity/test_unsigned_int_compare_zero.sol#L9
- solidity/test_unsigned_int_compare_zero.sol#L13

### severity:
Optimization

### category:
unsigned-int-compare-zero
