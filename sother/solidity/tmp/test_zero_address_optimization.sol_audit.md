## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | `revert CustomError()` should be used instead of `assert()` | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Assembly usage | 1 |
| [N-2] | Conformance to Solidity naming conventions | 3 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Using custom errors replace `require` or `assert` | 2 |
| [G-1] | Use assembly to check for `address(0)` | 3 |



## [Low] `revert CustomError()` should be used instead of `assert()`

### description:

Prior to solidity version 0.8.0, hitting an assert consumes the **remainder of the 
transaction's available gas** rather than returning it, as `require()`/`revert()` do. 
`assert()` should be avoided even past solidity version 0.8.0 as its 
[documentation](https://docs.soliditylang.org/en/latest/control-structures.html#panic-via-assert-and-error-via-require) 
states that "The assert function creates an error of type Panic(uint256). ... 
Properly functioning code should never create a Panic, not even on invalid external 
input. If this happens, then there is a bug in your contract which you should fix.



**There is `1` instance of this issue:**

- `assert(bool)(_addr != address(0))` (solidity/test_zero_address_optimization.sol#L4) should be replaced by `if (!condition) revert CustomError();`.


### recommendation:

Please use `if (!condition) revert CustomError();` instead of `assert()`.


### locations:
- solidity/test_zero_address_optimization.sol#L4

### severity:
Low

### category:
deprecated-assert

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

## [Informational] Assembly usage

### description:
The use of assembly is error-prone and should be avoided.

**There is `1` instance of this issue:**

- `Contract0.good(address)` (solidity/test_zero_address_optimization.sol#L14-L21) uses assembly
	- `INLINE ASM` (solidity/test_zero_address_optimization.sol#L15-L20)


### recommendation:
Do not use `evm` assembly.

### locations:
- solidity/test_zero_address_optimization.sol#L14-L21

### severity:
Informational

### category:
assembly

## [Informational] Conformance to Solidity naming conventions

### description:

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There are `3` instances of this issue:**

- Parameter `Contract0.bad(address)._addr` (solidity/test_zero_address_optimization.sol#L2) is not in mixedCase

- Parameter `Contract0.notBad(address)._addr` (solidity/test_zero_address_optimization.sol#L10) is not in mixedCase

- Parameter `Contract0.good(address)._addr` (solidity/test_zero_address_optimization.sol#L14) is not in mixedCase


### recommendation:
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations:
- solidity/test_zero_address_optimization.sol#L2
- solidity/test_zero_address_optimization.sol#L10
- solidity/test_zero_address_optimization.sol#L14

### severity:
Informational

### category:
naming-convention

## [Optimization] Using custom errors replace `require` or `assert`

### description:

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `2` instances of this issue:**

- `require(bool,string)(_addr != address(0),zero address))` (solidity/test_zero_address_optimization.sol#L3) should use custom error to save gas.

- `assert(bool)(_addr != address(0))` (solidity/test_zero_address_optimization.sol#L4) should use custom error to save gas.


### recommendation:

Using custom errors replace `require` or `assert`.


### locations:
- solidity/test_zero_address_optimization.sol#L3
- solidity/test_zero_address_optimization.sol#L4

### severity:
Optimization

### category:
use-custom-error

## [Optimization] Use assembly to check for `address(0)`

### description:

[Inline Assembly](https://docs.soliditylang.org/en/latest/assembly.html) more gas efficient and [Saving Gas with Simple Inlining](https://blog.soliditylang.org/2021/03/02/saving-gas-with-simple-inliner/).



**There are `3` instances of this issue:**

- `require(bool,string)(_addr != address(0),zero address))` (solidity/test_zero_address_optimization.sol#L3) should use assembly to check for `address(0)`

- `assert(bool)(_addr != address(0))` (solidity/test_zero_address_optimization.sol#L4) should use assembly to check for `address(0)`

- `_addr == address(0)` (solidity/test_zero_address_optimization.sol#L5) should use assembly to check for `address(0)`


### recommendation:

Use assembly to check for `address(0)`:

```
function addrNotZero(address _addr) public pure {
        assembly {
            if iszero(_addr) {
                mstore(0x00, "zero address")
                revert(0x00, 0x20)
            }
        }
}
```


### locations:
- solidity/test_zero_address_optimization.sol#L3
- solidity/test_zero_address_optimization.sol#L4
- solidity/test_zero_address_optimization.sol#L5

### severity:
Optimization

### category:
zero-address-optimization
