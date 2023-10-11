## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Unnecessary Public Function Modifier | 4 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Don't compare booleans to `true` or `false` | 2 |



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

**There are `4` instances of this issue:**

- function:[CompareTrue.bad(bool)](solidity/tmp/test_compare_true_false.sol#L2-L6)is public and can be replaced with external 

- function:[CompareTrue.bad2(bool)](solidity/tmp/test_compare_true_false.sol#L8-L12)is public and can be replaced with external 

- function:[CompareTrue.notBad(bool)](solidity/tmp/test_compare_true_false.sol#L14-L18)is public and can be replaced with external 

- function:[CompareTrue.notBad2(bool)](solidity/tmp/test_compare_true_false.sol#L20-L24)is public and can be replaced with external 

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
- solidity/tmp/test_compare_true_false.sol#L2-L6
- solidity/tmp/test_compare_true_false.sol#L8-L12
- solidity/tmp/test_compare_true_false.sol#L14-L18
- solidity/tmp/test_compare_true_false.sol#L20-L24

### severity
Informational

### category
unnecessary-public-function-modifier

### confidence
High

## [Optimization] Don't compare booleans to `true` or `false`

### description

`true` and `false` are constants and it is more expensive comparing a boolean against them 
than directly checking the returned boolean value


**There are `2` instances of this issue:**

- [CompareTrue.bad(bool)](solidity/tmp/test_compare_true_false.sol#L2-L6) compares to a boolean constant:
	-[a == true](solidity/tmp/test_compare_true_false.sol#L3)

- [CompareTrue.bad2(bool)](solidity/tmp/test_compare_true_false.sol#L8-L12) compares to a boolean constant:
	-[a == false](solidity/tmp/test_compare_true_false.sol#L9)

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

### recommendation
Remove the equality to the boolean constant.

### locations
- solidity/tmp/test_compare_true_false.sol#L2-L6
- solidity/tmp/test_compare_true_false.sol#L8-L12

### severity
Optimization

### category
boolean-equal

### confidence
High
