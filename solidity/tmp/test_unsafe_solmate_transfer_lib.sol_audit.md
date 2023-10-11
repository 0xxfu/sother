## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Solmate's `SafeTransferLib` doesn't check whether the ERC20 contract exists | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Assembly usage | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Using custom errors replace `require` or `assert` | 1 |
| [G-1] | Dead-code: functions not used should be removed to save deployment gas | 1 |



## [Low] Solmate's `SafeTransferLib` doesn't check whether the ERC20 contract exists

### description

Solmate's SafeTransferLib, which is often used to interact with non-compliant/unsafe ERC20 tokens, does not check whether the ERC20 contract exists. The following code will not revert in case the token doesn't exist (yet).

This is stated in the Solmate library: https://github.com/transmissions11/solmate/blob/main/src/utils/SafeTransferLib.sol#L9

Consider using OpenZeppelin's SafeERC20 library instead.


**There is `1` instance of this issue:**

-  Using OpenZeppelin's `SafeERC20` instead of `SafeTransferLib`.


### recommendation

Using OpenZeppelin's `SafeERC20` instead of Solmate's `SafeTransferLib`. 


### locations
- 

### severity
Low

### category
unsafe-solmate-transfer-lib

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

## [Informational] Assembly usage

### description
The use of assembly is error-prone and should be avoided.

**There is `1` instance of this issue:**

- [SafeTransferLib.safeTransferETH(address,uint256)](solidity/tmp/test_unsafe_solmate_transfer_lib.sol#L2-L12) uses assembly
	- [INLINE ASM](solidity/tmp/test_unsafe_solmate_transfer_lib.sol#L6-L9)


### recommendation
Do not use `evm` assembly.

### locations
- solidity/tmp/test_unsafe_solmate_transfer_lib.sol#L2-L12

### severity
Informational

### category
assembly

### confidence
High

## [Optimization] Using custom errors replace `require` or `assert`

### description

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There is `1` instance of this issue:**

- [require(bool,string)(success,"ETH_TRANSFER_FAILED")](solidity/tmp/test_unsafe_solmate_transfer_lib.sol#L11) should use custom error to save gas.


### recommendation

Using custom errors replace `require` or `assert`.


### locations
- solidity/tmp/test_unsafe_solmate_transfer_lib.sol#L11

### severity
Optimization

### category
use-custom-error

### confidence
High

## [Optimization] Dead-code: functions not used should be removed to save deployment gas

### description
Functions that are not sued.

**There is `1` instance of this issue:**

- [SafeTransferLib.safeTransferETH(address,uint256)](solidity/tmp/test_unsafe_solmate_transfer_lib.sol#L2-L12) is never used and should be removed


### recommendation
Remove unused functions.

### locations
- solidity/tmp/test_unsafe_solmate_transfer_lib.sol#L2-L12

### severity
Optimization

### category
dead-code

### confidence
High
