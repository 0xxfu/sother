## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | The result of function calls should be cached rather than re-calling the function | 2 |



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

## [Optimization] The result of function calls should be cached rather than re-calling the function

### description:

The instances below point to the second+ call of the function within a single function


**There are `2` instances of this issue:**

- `DivisionByZero.f0()` called result should be cached with local variable in [DivisionByZero.bad0(uint256,uint256)](solidity/division_by_zero.sol#L2-L10), It is called more than once:
	- [10 / (f0() * a)](solidity/division_by_zero.sol#L9)
	- [f0() / a](solidity/division_by_zero.sol#L5)

- `DivisionByZero.f0()` called result should be cached with local variable in [DivisionByZero.notBad0(uint256,uint256)](solidity/division_by_zero.sol#L12-L20), It is called more than once:
	- [10 / (f0() * a - 100)](solidity/division_by_zero.sol#L19)
	- [f0() / a - 1](solidity/division_by_zero.sol#L15)


### recommendation:

Using local variable to cache function called result if the same function called more than once.


### locations:
- solidity/division_by_zero.sol#L2-L10
- solidity/division_by_zero.sol#L12-L20

### severity:
Optimization

### category:
cache-call-function-result
