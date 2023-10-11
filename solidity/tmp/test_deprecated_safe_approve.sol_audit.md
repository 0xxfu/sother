## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Did not Approve to zero first | 1 |
| [M-1] | Unused return | 1 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | `safeApprove()` is deprecated | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Using custom errors replace `require` or `assert` | 1 |
| [G-1] | Use indexed events for value types as they are less costly compared to non-indexed ones | 2 |
| [G-2] | Shortening revert strings to fit in 32 `bytes` | 1 |



## [Medium] Did not Approve to zero first

### description

Calling `approve()` without first calling `approve(0)` if the current approval is non-zero 
will revert with some tokens, such as Tether (USDT). While Tether is known to do this, 
it applies to other tokens as well, which are trying to protect against 
[this attack vector](https://docs.google.com/document/d/1YLPtQxZu1UAvO9cZ1O2RPXBbT0mooh4DYKjA_jp-RLM/edit). 
`safeApprove()` itself also implements this protection.
Always reset the approval to zero before changing it to a new value, 
or use `safeIncreaseAllowance()`/`safeDecreaseAllowance()`



**There is `1` instance of this issue:**

- [erc20.approve(recipient,1)](solidity/tmp/test_deprecated_safe_approve.sol#L56) should be used `safeIncreaseAllowance()` or `safeDecreaseAllowance()` instead.

#### Exploit scenario

Some ERC20 tokens like `USDT` require resetting the approval to 0 first before being 
able to reset it to another value.

Unsafe ERC20 approve that do not handle non-standard erc20 behavior.
1. Some token contracts do not return any value.
2. Some token contracts revert the transaction when the allowance is not zero.


### recommendation

As suggested by the [OpenZeppelin comment](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/token/ERC20/utils/SafeERC20.sol#L38-L45),
replace `approve()/safeApprove()` with `safeIncreaseAllowance()` or `safeDecreaseAllowance()` instead.


### locations
- solidity/tmp/test_deprecated_safe_approve.sol#L56

### severity
Medium

### category
deprecated-approve

### confidence
High

## [Medium] Unused return

### description
The return value of an external call is not stored in a local or state variable.

**There is `1` instance of this issue:**

- [DeprecatedApprove.approveERC20(IERC20,address)](solidity/tmp/test_deprecated_safe_approve.sol#L55-L57) ignores return value by [erc20.approve(recipient,1)](solidity/tmp/test_deprecated_safe_approve.sol#L56)

#### Exploit scenario

```solidity
contract MyConc{
    using SafeMath for uint;   
    function my_func(uint a, uint b) public{
        a.add(b);
    }
}
```
`MyConc` calls `add` of `SafeMath`, but does not store the result in `a`. As a result, the computation has no effect.

### recommendation
Ensure that all the return values of the function calls are used.

### locations
- solidity/tmp/test_deprecated_safe_approve.sol#L55-L57

### severity
Medium

### category
unused-return

### confidence
Medium

## [Low] `safeApprove()` is deprecated

### description

[Deprecated](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/token/ERC20/utils/SafeERC20.sol#L38-L45) 
in favor of `safeIncreaseAllowance()` and `safeDecreaseAllowance()`. 
If only setting the initial allowance to the value that means infinite, 
`safeIncreaseAllowance()` can be used instead. The function may currently work, 
but if a bug is found in this version of OpenZeppelin, and the version that you're 
forced to upgrade to no longer has this function, you'll encounter unnecessary delays 
in porting and testing replacement contracts.



**There is `1` instance of this issue:**

- [erc20.safeApprove(recipient,1)](solidity/tmp/test_deprecated_safe_approve.sol#L50) is deprecated.


### recommendation

As suggested by the [OpenZeppelin comment](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/token/ERC20/utils/SafeERC20.sol#L38-L45),
replace `safeApprove()` with `safeIncreaseAllowance()` or `safeDecreaseAllowance()` instead.


### locations
- solidity/tmp/test_deprecated_safe_approve.sol#L50

### severity
Low

### category
deprecated-safe-approve

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

## [Optimization] Using custom errors replace `require` or `assert`

### description

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There is `1` instance of this issue:**

- [require(bool,string)((value == 0) || (token.allowance(address(this),spender) == 0),"SafeERC20: approve from non-zero to non-zero allowance")](solidity/tmp/test_deprecated_safe_approve.sol#L38-L41) should use custom error to save gas.


### recommendation

Using custom errors replace `require` or `assert`.


### locations
- solidity/tmp/test_deprecated_safe_approve.sol#L38-L41

### severity
Optimization

### category
use-custom-error

### confidence
High

## [Optimization] Use indexed events for value types as they are less costly compared to non-indexed ones

### description

Using the `indexed` keyword for [value types](https://docs.soliditylang.org/en/v0.8.20/types.html#value-types) (`bool/int/address/string/bytes`) saves gas costs, as seen in [this example](https://gist.github.com/0xxfu/c292a65ecb61cae6fd2090366ea0877e).

However, this is only the case for value types, whereas indexing [reference types](https://docs.soliditylang.org/en/v0.8.20/types.html#reference-types) (`array/struct`) are more expensive than their unindexed version.


**There are `2` instances of this issue:**

- The following variables should be indexed in [IERC20.Transfer(address,address,uint256)](solidity/tmp/test_deprecated_safe_approve.sol#L23):

	- [value](solidity/tmp/test_deprecated_safe_approve.sol#L23)

- The following variables should be indexed in [IERC20.Approval(address,address,uint256)](solidity/tmp/test_deprecated_safe_approve.sol#L25-L29):

	- [value](solidity/tmp/test_deprecated_safe_approve.sol#L28)


### recommendation

Using the `indexed` keyword for values types `bool/int/address/string/bytes` in event


### locations
- solidity/tmp/test_deprecated_safe_approve.sol#L23
- solidity/tmp/test_deprecated_safe_approve.sol#L25-L29

### severity
Optimization

### category
unindexed-event

### confidence
High

## [Optimization] Shortening revert strings to fit in 32 `bytes`

### description

In Solidity, the size of a string is not fixed and depends on the length of the string. 
Each character in a string requires 2 `bytes` of storage. 
Additionally, there is an overhead of 32 `bytes` to store the length of the string.

Shortening revert strings to fit in 32 bytes will decrease deployment time gas 
and will decrease runtime gas when the revert condition is met.


**There is `1` instance of this issue:**

- [require(bool,string)((value == 0) || (token.allowance(address(this),spender) == 0),"SafeERC20: approve from non-zero to non-zero allowance")](solidity/tmp/test_deprecated_safe_approve.sol#L38-L41) should be shortened strings to fit in 32 `bytes` (16 characters).


### recommendation

Shortening revert strings to fit in 32 `bytes`


### locations
- solidity/tmp/test_deprecated_safe_approve.sol#L38-L41

### severity
Optimization

### category
revert-long-strings

### confidence
High
