## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | `safeApprove()` is deprecated | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Use `calldata` instead of `memory` for function parameters | 2 |
| [G-1] | Use indexed events for value types as they are less costly compared to non-indexed ones | 2 |
| [G-2] | use custom errors instead of revert strings | 1 |



## [Low] `safeApprove()` is deprecated

### description:

[Deprecated](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/token/ERC20/utils/SafeERC20.sol#L38-L45) 
in favor of `safeIncreaseAllowance()` and `safeDecreaseAllowance()`. 
If only setting the initial allowance to the value that means infinite, 
`safeIncreaseAllowance()` can be used instead. The function may currently work, 
but if a bug is found in this version of OpenZeppelin, and the version that you're 
forced to upgrade to no longer has this function, you'll encounter unnecessary delays 
in porting and testing replacement contracts.



**There is `1` instance of this issue:**

- [erc20.safeApprove(recipient,1)](solidity/test_deprecated_safe_approve.sol#L51) is deprecated.


### recommendation:

As suggested by the [OpenZeppelin comment](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/token/ERC20/utils/SafeERC20.sol#L38-L45),
replace `safeApprove()` with `safeIncreaseAllowance()` or `safeDecreaseAllowance()` instead.


### locations:
- solidity/test_deprecated_safe_approve.sol#L51

### severity:
Low

### category:
deprecated-safe-approve

## [Optimization] Use `calldata` instead of `memory` for function parameters

### description:

On external functions, when using the `memory` keyword with a function argument, what's happening is a `memory` acts as an intermediate.

When the function gets called externally, the array values are kept in `calldata` and copied to memory during ABI decoding (using the opcode `calldataload` and `mstore`). 
And during the for loop, the values in the array are accessed in memory using a `mload`. That is inefficient. Reading directly from `calldata` using `calldataload` instead of going via `memory` saves the gas from the intermediate memory operations that carry the values.

More detail see [this](https://ethereum.stackexchange.com/questions/74442/when-should-i-use-calldata-and-when-should-i-use-memory)


**There are `2` instances of this issue:**

- [SafeERC20.safeApprove(IERC20,address,uint256)](solidity/test_deprecated_safe_approve.sol#L34-L44) read-only `memory` parameters below should be changed to `calldata` :
	- [SafeERC20.safeApprove(IERC20,address,uint256).token](solidity/test_deprecated_safe_approve.sol#L35)

- [DeprecatedSafeApprove.approveERC20(IERC20,address)](solidity/test_deprecated_safe_approve.sol#L50-L52) read-only `memory` parameters below should be changed to `calldata` :
	- [DeprecatedSafeApprove.approveERC20(IERC20,address).erc20](solidity/test_deprecated_safe_approve.sol#L50)


### recommendation:
Use `calldata` instead of `memory` for external functions where the function argument is read-only.

### locations:
- solidity/test_deprecated_safe_approve.sol#L34-L44
- solidity/test_deprecated_safe_approve.sol#L50-L52

### severity:
Optimization

### category:
memory-in-parameters

## [Optimization] Use indexed events for value types as they are less costly compared to non-indexed ones

### description:

Using the `indexed` keyword for [value types](https://docs.soliditylang.org/en/v0.8.20/types.html#value-types) (`bool/int/address/string/bytes`) saves gas costs, as seen in [this example](https://gist.github.com/0xxfu/c292a65ecb61cae6fd2090366ea0877e).

However, this is only the case for value types, whereas indexing [reference types](https://docs.soliditylang.org/en/v0.8.20/types.html#reference-types) (`array/struct`) are more expensive than their unindexed version.


**There are `2` instances of this issue:**

- The following variables should be indexed in [IERC20.Transfer(address,address,uint256)](solidity/test_deprecated_safe_approve.sol#L24):

	- [value](solidity/test_deprecated_safe_approve.sol#L24)

- The following variables should be indexed in [IERC20.Approval(address,address,uint256)](solidity/test_deprecated_safe_approve.sol#L26-L30):

	- [value](solidity/test_deprecated_safe_approve.sol#L29)


### recommendation:

Using the `indexed` keyword for values types `bool/int/address/string/bytes` in event


### locations:
- solidity/test_deprecated_safe_approve.sol#L24
- solidity/test_deprecated_safe_approve.sol#L26-L30

### severity:
Optimization

### category:
unindexed-event

## [Optimization] use custom errors instead of revert strings

### description:

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There is `1` instance of this issue:**

- [require(bool,string)((value == 0) || (token.allowance(address(this),spender) == 0),SafeERC20: approve from non-zero to non-zero allowance)](solidity/test_deprecated_safe_approve.sol#L39-L42) should use custom error to save gas.


### recommendation:

Using custom errors replace `require` or `assert`.


### locations:
- solidity/test_deprecated_safe_approve.sol#L39-L42

### severity:
Optimization

### category:
use-custom-error
