## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | `revert CustomError()` should be used instead of `assert()` | 1 |
| [L-1] | Missing array length equality checks may lead to incorrect or undefined behavior | 3 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | use custom errors instead of revert strings | 2 |



## [Low] `revert CustomError()` should be used instead of `assert()`

### description:

Prior to solidity version 0.8.0, hitting an assert consumes the **remainder of the transaction's available gas** rather than returning it, as `require()`/`revert()` do. `assert()` should be avoided even past solidity version 0.8.0 as its [documentation](https://docs.soliditylang.org/en/v0.8.19/control-structures.html#panic-via-assert-and-error-via-require) states that "The assert function creates an error of type Panic(uint256). ... Properly functioning code should never create a Panic, not even on invalid external input. If this happens, then there is a bug in your contract which you should fix.



**There is `1` instance of this issue:**

- [assert(bool)(arrayA.length == arrayC.length)](solidity/test_unchecked_array_length.sol#L72) should be replaced by `if (!condition) revert CustomError();`.


### recommendation:

Please use `if (!condition) revert CustomError();` instead of `assert()`.


### locations:
- solidity/test_unchecked_array_length.sol#L72

### severity:
Low

### category:
deprecated-assert

## [Low] Missing array length equality checks may lead to incorrect or undefined behavior

### description:

If the length of the arrays are not required to be of the same length, user operations may not be fully executed due to a mismatch in the number of items iterated over, versus the number of items provided in the second array


**There are `3` instances of this issue:**

- Missing check lengths of parameters below in function [UncheckedArrayLength.bad(uint256[],uint256,uint256[])](solidity/test_unchecked_array_length.sol#L2-L8):
	- [UncheckedArrayLength.bad(uint256[],uint256,uint256[]).arrayC](solidity/test_unchecked_array_length.sol#L5)
	- [UncheckedArrayLength.bad(uint256[],uint256,uint256[]).arrayA](solidity/test_unchecked_array_length.sol#L3)

- Missing check lengths of parameters below in function [UncheckedArrayLength.bad3(uint256[],uint256[],uint256[])](solidity/test_unchecked_array_length.sol#L18-L27):
	- [UncheckedArrayLength.bad3(uint256[],uint256[],uint256[]).arrayB](solidity/test_unchecked_array_length.sol#L20)
	- [UncheckedArrayLength.bad3(uint256[],uint256[],uint256[]).arrayC](solidity/test_unchecked_array_length.sol#L21)
	- [UncheckedArrayLength.bad3(uint256[],uint256[],uint256[]).arrayA](solidity/test_unchecked_array_length.sol#L19)

- Missing check lengths of parameters below in function [UncheckedArrayLength.bad2(uint256[],uint256[],uint256[])](solidity/test_unchecked_array_length.sol#L10-L16):
	- [UncheckedArrayLength.bad2(uint256[],uint256[],uint256[]).arrayB](solidity/test_unchecked_array_length.sol#L12)
	- [UncheckedArrayLength.bad2(uint256[],uint256[],uint256[]).arrayC](solidity/test_unchecked_array_length.sol#L13)
	- [UncheckedArrayLength.bad2(uint256[],uint256[],uint256[]).arrayA](solidity/test_unchecked_array_length.sol#L11)


### recommendation:

Check if the lengths of the array parameters are equal before use.


### locations:
- solidity/test_unchecked_array_length.sol#L2-L8
- solidity/test_unchecked_array_length.sol#L18-L27
- solidity/test_unchecked_array_length.sol#L10-L16

### severity:
Low

### category:
unchecked-array-length

## [Optimization] use custom errors instead of revert strings

### description:

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `2` instances of this issue:**

- [require(bool,string)(arrayA.length == arrayC.length,Length err)](solidity/test_unchecked_array_length.sol#L63) should use custom error to save gas.

- [assert(bool)(arrayA.length == arrayC.length)](solidity/test_unchecked_array_length.sol#L72) should use custom error to save gas.


### recommendation:

Using custom errors replace `require` or `assert`.


### locations:
- solidity/test_unchecked_array_length.sol#L63
- solidity/test_unchecked_array_length.sol#L72

### severity:
Optimization

### category:
use-custom-error
