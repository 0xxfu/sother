## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Not using the named return variables anywhere in the function is confusing | 3 |



## [Informational] Incorrect versions of Solidity

### description:

`solc` frequently releases new compiler versions. Using an old version prevents access to new Solidity security checks.
We also recommend avoiding complex `pragma` statement.

**There is `1` instance of this issue:**

- solc-0.8.19 is not recommended for deployment


### recommendation:

Deploy with any of the following Solidity versions:
- 0.8.21

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

### confidence:
High

## [Optimization] Not using the named return variables anywhere in the function is confusing

### description:

Consider changing the variable to be an unnamed one, 
since the variable is never assigned, nor is it returned by name. 
If the optimizer is not turned on, leaving the code as it is will also waste gas 
for the stack variable.


**There are `3` instances of this issue:**

- The named return variables in [UnusedReturnName.bad0()](solidity/test_unused_named_return_variables.sol#L2-L4) are unused.
	- [UnusedReturnName.bad0().a](solidity/test_unused_named_return_variables.sol#L2)

- The named return variables in [UnusedReturnName.bad1()](solidity/test_unused_named_return_variables.sol#L6-L9) are unused.
	- [UnusedReturnName.bad1().b](solidity/test_unused_named_return_variables.sol#L6)

- The named return variables in [UnusedReturnName.bad2()](solidity/test_unused_named_return_variables.sol#L11-L13) are unused.
	- [UnusedReturnName.bad2().a](solidity/test_unused_named_return_variables.sol#L11)
	- [UnusedReturnName.bad2().b](solidity/test_unused_named_return_variables.sol#L11)


### recommendation:

Remove the unused named return variables.


### locations:
- solidity/test_unused_named_return_variables.sol#L2-L4
- solidity/test_unused_named_return_variables.sol#L6-L9
- solidity/test_unused_named_return_variables.sol#L11-L13

### severity:
Optimization

### category:
unused-named-return-variables

### confidence:
High
