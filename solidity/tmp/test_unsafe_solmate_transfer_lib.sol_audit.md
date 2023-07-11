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
| [G-0] | Dead-code: functions not used should be removed to save deployment gas | 1 |
| [G-1] | Shortening revert strings to fit in 32 `bytes` | 1 |
| [G-2] | Using custom errors replace `require` or `assert` | 1 |



## [Low] Solmate's `SafeTransferLib` doesn't check whether the ERC20 contract exists

### description:

Solmate's SafeTransferLib, which is often used to interact with non-compliant/unsafe ERC20 tokens, does not check whether the ERC20 contract exists. The following code will not revert in case the token doesn't exist (yet).

This is stated in the Solmate library: https://github.com/transmissions11/solmate/blob/main/src/utils/SafeTransferLib.sol#L9

Consider using OpenZeppelin's SafeERC20 library instead.


**There is `1` instance of this issue:**

-  Using OpenZeppelin's `SafeERC20` instead of `SafeTransferLib`.


### recommendation:

Using OpenZeppelin's `SafeERC20` instead of Solmate's `SafeTransferLib`. 


### locations:
- 

### severity:
Low

### category:
unsafe-solmate-transfer-lib

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

- [SafeTransferLib.safeTransferETH(address,uint256)](solidity/test_unsafe_solmate_transfer_lib.sol#L2-L12) uses assembly
	- [INLINE ASM](solidity/test_unsafe_solmate_transfer_lib.sol#L6-L9)


### recommendation:
Do not use `evm` assembly.

### locations:
- solidity/test_unsafe_solmate_transfer_lib.sol#L2-L12

### severity:
Informational

### category:
assembly

## [Optimization] Dead-code: functions not used should be removed to save deployment gas

### description:
Functions that are not sued.

**There is `1` instance of this issue:**

- [SafeTransferLib.safeTransferETH(address,uint256)](solidity/test_unsafe_solmate_transfer_lib.sol#L2-L12) is never used and should be removed


### recommendation:
Remove unused functions.

### locations:
- solidity/test_unsafe_solmate_transfer_lib.sol#L2-L12

### severity:
Optimization

### category:
dead-code

## [Optimization] Shortening revert strings to fit in 32 `bytes`

### description:

In Solidity, the size of a string is not fixed and depends on the length of the string. 
Each character in a string requires 2 `bytes` of storage. 
Additionally, there is an overhead of 32 `bytes` to store the length of the string.

Shortening revert strings to fit in 32 bytes will decrease deployment time gas 
and will decrease runtime gas when the revert condition is met.


**There is `1` instance of this issue:**

- [require(bool,string)(success,ETH_TRANSFER_FAILED)](solidity/test_unsafe_solmate_transfer_lib.sol#L11) should be shortened strings to fit in 32 `bytes` (16 characters).


### recommendation:

Shortening revert strings to fit in 32 `bytes`


### locations:
- solidity/test_unsafe_solmate_transfer_lib.sol#L11

### severity:
Optimization

### category:
revert-long-strings

## [Optimization] Using custom errors replace `require` or `assert`

### description:

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There is `1` instance of this issue:**

- [require(bool,string)(success,ETH_TRANSFER_FAILED)](solidity/test_unsafe_solmate_transfer_lib.sol#L11) should use custom error to save gas.


### recommendation:

Using custom errors replace `require` or `assert`.


### locations:
- solidity/test_unsafe_solmate_transfer_lib.sol#L11

### severity:
Optimization

### category:
use-custom-error
