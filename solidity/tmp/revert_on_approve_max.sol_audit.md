## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Did not Approve to zero first | 2 |
| [M-1] | Unused return | 2 |
| [M-2] | Void function | 3 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | `safeApprove()` is deprecated | 2 |
| [L-1] | Approve `type(uint256).max` not work with some tokens | 3 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Remove unused parameter variables | 3 |
| [G-1] | Dead-code: functions not used should be removed to save deployment gas | 1 |
| [G-2] | Empty blocks should be removed or emit something | 3 |



## [Medium] Did not Approve to zero first

### description

Calling `approve()` without first calling `approve(0)` if the current approval is non-zero 
will revert with some tokens, such as Tether (USDT). While Tether is known to do this, 
it applies to other tokens as well, which are trying to protect against 
[this attack vector](https://docs.google.com/document/d/1YLPtQxZu1UAvO9cZ1O2RPXBbT0mooh4DYKjA_jp-RLM/edit). 
`safeApprove()` itself also implements this protection.
Always reset the approval to zero before changing it to a new value, 
or use `safeIncreaseAllowance()`/`safeDecreaseAllowance()`



**There are `2` instances of this issue:**

- [token.approve(spender,type()(uint256).max)](solidity/tmp/revert_on_approve_max.sol#L34) should be used `safeIncreaseAllowance()` or `safeDecreaseAllowance()` instead.

- [token.approve(spender,type()(uint96).max)](solidity/tmp/revert_on_approve_max.sol#L42) should be used `safeIncreaseAllowance()` or `safeDecreaseAllowance()` instead.

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
- solidity/tmp/revert_on_approve_max.sol#L34
- solidity/tmp/revert_on_approve_max.sol#L42

### severity
Medium

### category
deprecated-approve

### confidence
High

## [Medium] Unused return

### description
The return value of an external call is not stored in a local or state variable.

**There are `2` instances of this issue:**

- [RevertOnApproveMax.bad(IERC20,address)](solidity/tmp/revert_on_approve_max.sol#L33-L39) ignores return value by [token.approve(spender,type()(uint256).max)](solidity/tmp/revert_on_approve_max.sol#L34)

- [RevertOnApproveMax.notBad(IERC20,address)](solidity/tmp/revert_on_approve_max.sol#L41-L47) ignores return value by [token.approve(spender,type()(uint96).max)](solidity/tmp/revert_on_approve_max.sol#L42)

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
- solidity/tmp/revert_on_approve_max.sol#L33-L39
- solidity/tmp/revert_on_approve_max.sol#L41-L47

### severity
Medium

### category
unused-return

### confidence
Medium

## [Medium] Void function

### description
Detect the call to a function that is not implemented

**There are `3` instances of this issue:**

- function:[SafeERC20.safeApprove(IERC20,address,uint256)](solidity/tmp/revert_on_approve_max.sol#L2-L6)is empty 

- function:[SafeERC20.safeIncreaseAllowance(IERC20,address,uint256)](solidity/tmp/revert_on_approve_max.sol#L8-L12)is empty 

- function:[SafeERC20.safeDecreaseAllowance(IERC20,address,uint256)](solidity/tmp/revert_on_approve_max.sol#L14-L18)is empty 

#### Exploit scenario

```solidity
contract A{}
contract B is A{
    constructor() public A(){}
}
```
When reading `B`'s constructor definition, we might assume that `A()` initiates the contract, but no code is executed.

### recommendation
Implement the function

### locations
- solidity/tmp/revert_on_approve_max.sol#L2-L6
- solidity/tmp/revert_on_approve_max.sol#L8-L12
- solidity/tmp/revert_on_approve_max.sol#L14-L18

### severity
Medium

### category
void-function

### confidence
High

## [Low] `safeApprove()` is deprecated

### description

[Deprecated](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/token/ERC20/utils/SafeERC20.sol#L38-L45) 
in favor of `safeIncreaseAllowance()` and `safeDecreaseAllowance()`. 
If only setting the initial allowance to the value that means infinite, 
`safeIncreaseAllowance()` can be used instead. The function may currently work, 
but if a bug is found in this version of OpenZeppelin, and the version that you're 
forced to upgrade to no longer has this function, you'll encounter unnecessary delays 
in porting and testing replacement contracts.



**There are `2` instances of this issue:**

- [token.safeApprove(spender,type()(uint256).max)](solidity/tmp/revert_on_approve_max.sol#L36) is deprecated.

- [token.safeApprove(spender,type()(uint96).max)](solidity/tmp/revert_on_approve_max.sol#L44) is deprecated.


### recommendation

As suggested by the [OpenZeppelin comment](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/token/ERC20/utils/SafeERC20.sol#L38-L45),
replace `safeApprove()` with `safeIncreaseAllowance()` or `safeDecreaseAllowance()` instead.


### locations
- solidity/tmp/revert_on_approve_max.sol#L36
- solidity/tmp/revert_on_approve_max.sol#L44

### severity
Low

### category
deprecated-safe-approve

### confidence
High

## [Low] Approve `type(uint256).max` not work with some tokens

### description

Some tokens (e.g. `UNI`, `COMP`) revert if the value passed to `approve` or `transfer` 
is larger than `uint96`.

Both of the above tokens have special case logic in `approve` that sets `allowance` 
to `type(uint96).max` if the `approval` amount is `uint256(-1)`, which may cause 
issues with systems that expect the value passed to `approve` to be reflected in 
the allowances mapping.

Approving the maximum value of `uint256` is a known practice to save gas. 
However, this pattern was proven to increase the impact of an attack many times in the past, 
in case the approved contract gets hacked.


**There are `3` instances of this issue:**

- [token.approve(spender,type()(uint256).max)](solidity/tmp/revert_on_approve_max.sol#L34) should use exact amount that's needed to be transferred.

- [token.safeApprove(spender,type()(uint256).max)](solidity/tmp/revert_on_approve_max.sol#L36) should use exact amount that's needed to be transferred.

- [token.safeIncreaseAllowance(spender,type()(uint256).max)](solidity/tmp/revert_on_approve_max.sol#L38) should use exact amount that's needed to be transferred.


### recommendation

Consider approving the exact amount that’s needed to be transferred 
instead of the `type(uint256).max` amount.


### locations
- solidity/tmp/revert_on_approve_max.sol#L34
- solidity/tmp/revert_on_approve_max.sol#L36
- solidity/tmp/revert_on_approve_max.sol#L38

### severity
Low

### category
revert-on-approve-max

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

## [Optimization] Remove unused parameter variables

### description

Unused parameters variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 



**There are `3` instances of this issue:**

- The param variables in [SafeERC20.safeApprove(IERC20,address,uint256)](solidity/tmp/revert_on_approve_max.sol#L2-L6) are unused.
	- [SafeERC20.safeApprove(IERC20,address,uint256).spender](solidity/tmp/revert_on_approve_max.sol#L4)
	- [SafeERC20.safeApprove(IERC20,address,uint256).token](solidity/tmp/revert_on_approve_max.sol#L3)
	- [SafeERC20.safeApprove(IERC20,address,uint256).value](solidity/tmp/revert_on_approve_max.sol#L5)

- The param variables in [SafeERC20.safeIncreaseAllowance(IERC20,address,uint256)](solidity/tmp/revert_on_approve_max.sol#L8-L12) are unused.
	- [SafeERC20.safeIncreaseAllowance(IERC20,address,uint256).token](solidity/tmp/revert_on_approve_max.sol#L9)
	- [SafeERC20.safeIncreaseAllowance(IERC20,address,uint256).spender](solidity/tmp/revert_on_approve_max.sol#L10)
	- [SafeERC20.safeIncreaseAllowance(IERC20,address,uint256).value](solidity/tmp/revert_on_approve_max.sol#L11)

- The param variables in [SafeERC20.safeDecreaseAllowance(IERC20,address,uint256)](solidity/tmp/revert_on_approve_max.sol#L14-L18) are unused.
	- [SafeERC20.safeDecreaseAllowance(IERC20,address,uint256).token](solidity/tmp/revert_on_approve_max.sol#L15)
	- [SafeERC20.safeDecreaseAllowance(IERC20,address,uint256).spender](solidity/tmp/revert_on_approve_max.sol#L16)
	- [SafeERC20.safeDecreaseAllowance(IERC20,address,uint256).value](solidity/tmp/revert_on_approve_max.sol#L17)


### recommendation

Remove the unused parameter variables.


### locations
- solidity/tmp/revert_on_approve_max.sol#L2-L6
- solidity/tmp/revert_on_approve_max.sol#L8-L12
- solidity/tmp/revert_on_approve_max.sol#L14-L18

### severity
Optimization

### category
unused-parameter

### confidence
High

## [Optimization] Dead-code: functions not used should be removed to save deployment gas

### description
Functions that are not sued.

**There is `1` instance of this issue:**

- [SafeERC20.safeDecreaseAllowance(IERC20,address,uint256)](solidity/tmp/revert_on_approve_max.sol#L14-L18) is never used and should be removed


### recommendation
Remove unused functions.

### locations
- solidity/tmp/revert_on_approve_max.sol#L14-L18

### severity
Optimization

### category
dead-code

### confidence
High

## [Optimization] Empty blocks should be removed or emit something

### description

The code should be refactored such that they no longer exist, or the block should do 
something useful, such as emitting an event or reverting. 
If the contract is meant to be extended, the contract should be `abstract` and the function 
signatures be added without any default implementation.


**There are `3` instances of this issue:**

- [SafeERC20.safeApprove(IERC20,address,uint256)](solidity/tmp/revert_on_approve_max.sol#L2-L6) should removed or do something

- [SafeERC20.safeIncreaseAllowance(IERC20,address,uint256)](solidity/tmp/revert_on_approve_max.sol#L8-L12) should removed or do something

- [SafeERC20.safeDecreaseAllowance(IERC20,address,uint256)](solidity/tmp/revert_on_approve_max.sol#L14-L18) should removed or do something


### recommendation

Empty blocks should emit an event, or revert. 
If not, they can simply be removed to save gas upon deployment. 
This is valid for `receive()` functions, but also `constructors()`


### locations
- solidity/tmp/revert_on_approve_max.sol#L2-L6
- solidity/tmp/revert_on_approve_max.sol#L8-L12
- solidity/tmp/revert_on_approve_max.sol#L14-L18

### severity
Optimization

### category
empty-block

### confidence
High
