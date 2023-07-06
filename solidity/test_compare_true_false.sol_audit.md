## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Don't compare booleans to `true` or `false` | 2 |



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

## [Optimization] Don't compare booleans to `true` or `false`

### description:

`true` and `false` are constants and it is more expensive comparing a boolean against them 
than directly checking the returned boolean value


**There are `2` instances of this issue:**

- `CompareTrue.bad(bool)` (solidity/test_compare_true_false.sol#L2-L6) compares to a boolean constant:
	-`a == true` (solidity/test_compare_true_false.sol#L3)

- `CompareTrue.bad2(bool)` (solidity/test_compare_true_false.sol#L8-L12) compares to a boolean constant:
	-`a == false` (solidity/test_compare_true_false.sol#L9)

#### Exploit scenario

```solidity
contract A {
	function f(bool x) public {
		// ...
        if (x == true) { // bad!
           // ...
        }
		// ...
	}
}
```
Boolean constants can be used directly and do not need to be compare to `true` or `false`.

### recommendation:
Remove the equality to the boolean constant.

### locations:
- solidity/test_compare_true_false.sol#L2-L6
- solidity/test_compare_true_false.sol#L8-L12

### severity:
Optimization

### category:
boolean-equal
