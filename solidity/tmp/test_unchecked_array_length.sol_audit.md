## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Missing array length equality checks may lead to incorrect or undefined behavior | 3 |
| [L-1] | `revert CustomError()` should be used instead of `assert()` | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Unnecessary Public Function Modifier | 8 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Using custom errors replace `require` or `assert` | 2 |
| [G-1] | Remove unused parameter variables | 7 |



## [Low] Missing array length equality checks may lead to incorrect or undefined behavior

### description

If the length of the arrays are not required to be of the same length, user operations may not be fully executed due to a mismatch in the number of items iterated over, versus the number of items provided in the second array


**There are `3` instances of this issue:**

- Missing check lengths of parameters below in function [UncheckedArrayLength.bad(uint256[],uint256,uint256[])](solidity/tmp/test_unchecked_array_length.sol#L2-L8):
	- [UncheckedArrayLength.bad(uint256[],uint256,uint256[]).arrayC](solidity/tmp/test_unchecked_array_length.sol#L5)
	- [UncheckedArrayLength.bad(uint256[],uint256,uint256[]).arrayA](solidity/tmp/test_unchecked_array_length.sol#L3)

- Missing check lengths of parameters below in function [UncheckedArrayLength.bad2(uint256[],uint256[],uint256[])](solidity/tmp/test_unchecked_array_length.sol#L10-L16):
	- [UncheckedArrayLength.bad2(uint256[],uint256[],uint256[]).arrayA](solidity/tmp/test_unchecked_array_length.sol#L11)
	- [UncheckedArrayLength.bad2(uint256[],uint256[],uint256[]).arrayB](solidity/tmp/test_unchecked_array_length.sol#L12)
	- [UncheckedArrayLength.bad2(uint256[],uint256[],uint256[]).arrayC](solidity/tmp/test_unchecked_array_length.sol#L13)

- Missing check lengths of parameters below in function [UncheckedArrayLength.bad3(uint256[],uint256[],uint256[])](solidity/tmp/test_unchecked_array_length.sol#L18-L27):
	- [UncheckedArrayLength.bad3(uint256[],uint256[],uint256[]).arrayA](solidity/tmp/test_unchecked_array_length.sol#L19)
	- [UncheckedArrayLength.bad3(uint256[],uint256[],uint256[]).arrayB](solidity/tmp/test_unchecked_array_length.sol#L20)
	- [UncheckedArrayLength.bad3(uint256[],uint256[],uint256[]).arrayC](solidity/tmp/test_unchecked_array_length.sol#L21)


### recommendation

Check if the lengths of the array parameters are equal before use.


### locations
- solidity/tmp/test_unchecked_array_length.sol#L2-L8
- solidity/tmp/test_unchecked_array_length.sol#L10-L16
- solidity/tmp/test_unchecked_array_length.sol#L18-L27

### severity
Low

### category
unchecked-array-length

### confidence
High

## [Low] `revert CustomError()` should be used instead of `assert()`

### description

Prior to solidity version 0.8.0, hitting an assert consumes the **remainder of the 
transaction's available gas** rather than returning it, as `require()`/`revert()` do. 
`assert()` should be avoided even past solidity version 0.8.0 as its 
[documentation](https://docs.soliditylang.org/en/latest/control-structures.html#panic-via-assert-and-error-via-require) 
states that "The assert function creates an error of type Panic(uint256). ... 
Properly functioning code should never create a Panic, not even on invalid external 
input. If this happens, then there is a bug in your contract which you should fix.



**There is `1` instance of this issue:**

- [assert(bool)(arrayA.length == arrayC.length)](solidity/tmp/test_unchecked_array_length.sol#L72) should be replaced by `if (!condition) revert CustomError();`.


### recommendation

Please use `if (!condition) revert CustomError();` instead of `assert()`.


### locations
- solidity/tmp/test_unchecked_array_length.sol#L72

### severity
Low

### category
deprecated-assert

### confidence
High

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

**There are `8` instances of this issue:**

- function:[UncheckedArrayLength.bad(uint256[],uint256,uint256[])](solidity/tmp/test_unchecked_array_length.sol#L2-L8)is public and can be replaced with external 

- function:[UncheckedArrayLength.bad2(uint256[],uint256[],uint256[])](solidity/tmp/test_unchecked_array_length.sol#L10-L16)is public and can be replaced with external 

- function:[UncheckedArrayLength.bad3(uint256[],uint256[],uint256[])](solidity/tmp/test_unchecked_array_length.sol#L18-L27)is public and can be replaced with external 

- function:[UncheckedArrayLength.notBad(uint256[],uint256)](solidity/tmp/test_unchecked_array_length.sol#L29-L34)is public and can be replaced with external 

- function:[UncheckedArrayLength.goodWithRevert(uint256[],uint256,uint256[])](solidity/tmp/test_unchecked_array_length.sol#L36-L45)is public and can be replaced with external 

- function:[UncheckedArrayLength.goodWithRevert2(uint256[],uint256[],uint256[])](solidity/tmp/test_unchecked_array_length.sol#L47-L56)is public and can be replaced with external 

- function:[UncheckedArrayLength.goodWithRequire(uint256[],uint256,uint256[])](solidity/tmp/test_unchecked_array_length.sol#L58-L65)is public and can be replaced with external 

- function:[UncheckedArrayLength.goodWithAssert(uint256[],uint256,uint256[])](solidity/tmp/test_unchecked_array_length.sol#L67-L74)is public and can be replaced with external 

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
- solidity/tmp/test_unchecked_array_length.sol#L2-L8
- solidity/tmp/test_unchecked_array_length.sol#L10-L16
- solidity/tmp/test_unchecked_array_length.sol#L18-L27
- solidity/tmp/test_unchecked_array_length.sol#L29-L34
- solidity/tmp/test_unchecked_array_length.sol#L36-L45
- solidity/tmp/test_unchecked_array_length.sol#L47-L56
- solidity/tmp/test_unchecked_array_length.sol#L58-L65
- solidity/tmp/test_unchecked_array_length.sol#L67-L74

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


**There are `2` instances of this issue:**

- [require(bool,string)(arrayA.length == arrayC.length,"Length err")](solidity/tmp/test_unchecked_array_length.sol#L63) should use custom error to save gas.

- [assert(bool)(arrayA.length == arrayC.length)](solidity/tmp/test_unchecked_array_length.sol#L72) should use custom error to save gas.


### recommendation

Using custom errors replace `require` or `assert`.


### locations
- solidity/tmp/test_unchecked_array_length.sol#L63
- solidity/tmp/test_unchecked_array_length.sol#L72

### severity
Optimization

### category
use-custom-error

### confidence
High

## [Optimization] Remove unused parameter variables

### description

Unused parameters variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 



**There are `7` instances of this issue:**

- The param variables in [UncheckedArrayLength.bad(uint256[],uint256,uint256[])](solidity/tmp/test_unchecked_array_length.sol#L2-L8) are unused.
	- [UncheckedArrayLength.bad(uint256[],uint256,uint256[]).arrayC](solidity/tmp/test_unchecked_array_length.sol#L5)
	- [UncheckedArrayLength.bad(uint256[],uint256,uint256[]).arrayA](solidity/tmp/test_unchecked_array_length.sol#L3)
	- [UncheckedArrayLength.bad(uint256[],uint256,uint256[]).b](solidity/tmp/test_unchecked_array_length.sol#L4)

- The param variables in [UncheckedArrayLength.bad2(uint256[],uint256[],uint256[])](solidity/tmp/test_unchecked_array_length.sol#L10-L16) are unused.
	- [UncheckedArrayLength.bad2(uint256[],uint256[],uint256[]).arrayA](solidity/tmp/test_unchecked_array_length.sol#L11)
	- [UncheckedArrayLength.bad2(uint256[],uint256[],uint256[]).arrayB](solidity/tmp/test_unchecked_array_length.sol#L12)
	- [UncheckedArrayLength.bad2(uint256[],uint256[],uint256[]).arrayC](solidity/tmp/test_unchecked_array_length.sol#L13)

- The param variables in [UncheckedArrayLength.bad3(uint256[],uint256[],uint256[])](solidity/tmp/test_unchecked_array_length.sol#L18-L27) are unused.
	- [UncheckedArrayLength.bad3(uint256[],uint256[],uint256[]).arrayB](solidity/tmp/test_unchecked_array_length.sol#L20)

- The param variables in [UncheckedArrayLength.notBad(uint256[],uint256)](solidity/tmp/test_unchecked_array_length.sol#L29-L34) are unused.
	- [UncheckedArrayLength.notBad(uint256[],uint256).arrayA](solidity/tmp/test_unchecked_array_length.sol#L30)
	- [UncheckedArrayLength.notBad(uint256[],uint256).b](solidity/tmp/test_unchecked_array_length.sol#L31)

- The param variables in [UncheckedArrayLength.goodWithRevert(uint256[],uint256,uint256[])](solidity/tmp/test_unchecked_array_length.sol#L36-L45) are unused.
	- [UncheckedArrayLength.goodWithRevert(uint256[],uint256,uint256[]).b](solidity/tmp/test_unchecked_array_length.sol#L38)

- The param variables in [UncheckedArrayLength.goodWithRequire(uint256[],uint256,uint256[])](solidity/tmp/test_unchecked_array_length.sol#L58-L65) are unused.
	- [UncheckedArrayLength.goodWithRequire(uint256[],uint256,uint256[]).b](solidity/tmp/test_unchecked_array_length.sol#L60)

- The param variables in [UncheckedArrayLength.goodWithAssert(uint256[],uint256,uint256[])](solidity/tmp/test_unchecked_array_length.sol#L67-L74) are unused.
	- [UncheckedArrayLength.goodWithAssert(uint256[],uint256,uint256[]).b](solidity/tmp/test_unchecked_array_length.sol#L69)


### recommendation

Remove the unused parameter variables.


### locations
- solidity/tmp/test_unchecked_array_length.sol#L2-L8
- solidity/tmp/test_unchecked_array_length.sol#L10-L16
- solidity/tmp/test_unchecked_array_length.sol#L18-L27
- solidity/tmp/test_unchecked_array_length.sol#L29-L34
- solidity/tmp/test_unchecked_array_length.sol#L36-L45
- solidity/tmp/test_unchecked_array_length.sol#L58-L65
- solidity/tmp/test_unchecked_array_length.sol#L67-L74

### severity
Optimization

### category
unused-parameter

### confidence
High
