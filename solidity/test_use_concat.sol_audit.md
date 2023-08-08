## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Pre-calculate the results into `constant` instead of calculate `keccak256`/`abi.encode**` in runtime. | 1 |
| [G-1] | Expression `""` is cheaper than `new bytes(0)` | 5 |
| [G-2] | Use `string.concat()` on string instead of `abi.encodePacked()` to save gas | 1 |
| [G-3] | Use `bytes.concat()` on mixing bytes and strings instead of `abi.encodePacked()` to save gas | 2 |



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

## [Optimization] Pre-calculate the results into `constant` instead of calculate `keccak256`/`abi.encode**` in runtime.

### description:

It should be saved to an `constant` variable, and the `constant` used instead. 
If the hash is being used as a part of a function selector, 
the cast to bytes4 should only be Pre-calculated


**There is `1` instance of this issue:**

- [abi.encodePacked(a)](solidity/test_use_concat.sol#L4) should use pre-calculate results instead of calculation in runtime.


### recommendation:

Pre-calculate the results(hardcode) into `constant` instead of calculate `keccak256`/`abi.encode**` in runtime.


### locations:
- solidity/test_use_concat.sol#L4

### severity:
Optimization

### category:
keccak-constant-in-function

### confidence:
High

## [Optimization] Expression `""` is cheaper than `new bytes(0)`

### description:




**There are `5` instances of this issue:**

- Should use `""` instead of `new bytes(0)` on [abi.encodePacked(a,new bytes(0))](solidity/test_use_concat.sol#L6)

- Should use `""` instead of `new bytes(0)` on [bytes.concat(new bytes(0),new bytes(0))](solidity/test_use_concat.sol#L15)

- Should use `""` instead of `new bytes(0)` on [bytes.concat(a,new bytes(0))](solidity/test_use_concat.sol#L17)

- Should use `""` instead of `new bytes(0)` on [abi.encodePacked(new bytes(0))](solidity/test_use_concat.sol#L21)

- Should use `""` instead of `new bytes(0)` on [abi.encodePacked(new bytes(0),new bytes(0))](solidity/test_use_concat.sol#L22)


### recommendation:

Using empty string `""` instead of `new bytes(0)`.


### locations:
- solidity/test_use_concat.sol#L6
- solidity/test_use_concat.sol#L15
- solidity/test_use_concat.sol#L17
- solidity/test_use_concat.sol#L21
- solidity/test_use_concat.sol#L22

### severity:
Optimization

### category:
inefficient-new-bytes

### confidence:
High

## [Optimization] Use `string.concat()` on string instead of `abi.encodePacked()` to save gas

### description:

Starting with version 0.8.12, 
Solidity has the `string.concat()` function, 
which allows one to concatenate a list of strings, without extra padding. 
Using this function rather than `abi.encodePacked()` makes the intended operation more clear, 
leading to less reviewer confusion and saving more gas.


**There is `1` instance of this issue:**

- should use `string.concat()` on string instead of [abi.encodePacked(a)](solidity/test_use_concat.sol#L4)


### recommendation:

Use `string.concat()` on string instead of `abi.encodePacked()`


### locations:
- solidity/test_use_concat.sol#L4

### severity:
Optimization

### category:
use-concat-on-string

### confidence:
High

## [Optimization] Use `bytes.concat()` on mixing bytes and strings instead of `abi.encodePacked()` to save gas

### description:

Starting with version 0.8.4, 
Solidity has the `bytes.concat()` function, 
which allows one to concatenate a list of bytes/strings, without extra padding. 
Using this function rather than `abi.encodePacked()` makes the intended operation more clear, 
leading to less reviewer confusion and saving more gas.


**There are `2` instances of this issue:**

- should use `bytes.concat()` on mixing bytes and strings instead of  [abi.encodePacked(a,new bytes(0))](solidity/test_use_concat.sol#L6)

- should use `bytes.concat()` on mixing bytes and strings instead of  [abi.encodePacked(a,bytes32(0))](solidity/test_use_concat.sol#L8)


### recommendation:

Use `bytes.concat()` on mixing bytes and strings instead of `abi.encodePacked()`


### locations:
- solidity/test_use_concat.sol#L6
- solidity/test_use_concat.sol#L8

### severity:
Optimization

### category:
use-concat-on-bytes

### confidence:
High
