## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | Uninitialized state variables | 1 |
| [H-1] | State variable not initialized | 1 |


### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Return values of `transfer()/transferFrom()` not checked | 4 |
| [M-1] | Unsafe use of `transfer()/transferFrom()` with IERC20 | 4 |
| [M-2] | Void function | 1 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Functions calling contracts/addresses with transfer hooks are missing reentrancy guards | 4 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Cache state variables instead of rereading | 4 |
| [G-1] | Remove unused parameter variables | 1 |
| [G-2] | Remove unused local variables | 2 |
| [G-3] | Amounts should be checked for `0` before calling a `transfer` | 8 |
| [G-4] | Empty blocks should be removed or emit something | 1 |
| [G-5] | State variables that could be declared constant | 1 |



## [High] Uninitialized state variables

### description
Uninitialized state variables.

**There is `1` instance of this issue:**

- [ReentrancyTransfer.token](solidity/tmp/test_reentrancy_transfer.sol#L42) is never initialized. It is used in:
	- [ReentrancyTransfer.bad0(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L47-L50)
	- [ReentrancyTransfer.bad1(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L52-L55)
	- [ReentrancyTransfer.good0(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L57-L62)
	- [ReentrancyTransfer.good1(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L64-L69)

#### Exploit scenario

```solidity
contract Uninitialized{
    address destination;

    function transfer() payable public{
        destination.transfer(msg.value);
    }
}
```
Bob calls `transfer`. As a result, the Ether are sent to the address `0x0` and are lost.


### recommendation

Initialize all the variables. If a variable is meant to be initialized to zero, explicitly set it to zero to improve code readability.


### locations
- solidity/tmp/test_reentrancy_transfer.sol#L42

### severity
High

### category
uninitialized-state

### confidence
High

## [High] State variable not initialized

### description
A state variable not initialized and not written in contract but be used in contract

**There is `1` instance of this issue:**

- state variable: [ReentrancyTransfer.token](solidity/tmp/test_reentrancy_transfer.sol#L42) not initialized and not written in contract but be used in contract

#### Exploit scenario

```solidity
    struct BalancesStruct{
        address owner;
        array[]] balances;
    }
    array[] public stackBalance;

    function remove() internal{
         delete stackBalance[msg.sender];
    }
```
`remove` deletes an item of `stackBalance`.
The array `balances` is never deleted, so `remove` does not work as intended.

### recommendation
Use a lock mechanism instead of a deletion to disable structure containing a array.

### locations
- solidity/tmp/test_reentrancy_transfer.sol#L42

### severity
High

### category
state-variable-not-initialized

### confidence
High

## [Medium] Return values of `transfer()/transferFrom()` not checked

### description

Not all `IERC20` implementations `revert()` when there's a failure in `transfer()`/`transferFrom()`. The function signature has a `boolean` return value and they indicate errors that way instead. By not checking the return value, operations that should have marked as failed, may potentially go through without actually making a payment.


**There are `4` instances of this issue:**

- [ReentrancyTransfer.bad0(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L47-L50) ignores return value by [token.transferFrom(address(this),to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L49)

- [ReentrancyTransfer.bad0(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L47-L50) ignores return value by [token.transfer(to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L48)

- [ReentrancyTransfer.good0(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L57-L62) ignores return value by [token.transfer(to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L59)

- [ReentrancyTransfer.good0(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L57-L62) ignores return value by [token.transferFrom(address(this),to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L60)

#### Exploit scenario

```solidity
contract Token {
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);
}
contract MyBank{  
    mapping(address => uint) balances;
    Token token;
    function deposit(uint amount) public{
        token.transferFrom(msg.sender, address(this), amount);
        balances[msg.sender] += amount;
    }
}
```
Several tokens do not revert in case of failure and return false. If one of these tokens is used in `MyBank`, `deposit` will not revert if the transfer fails, and an attacker can call `deposit` for free..

### recommendation
Use `SafeERC20`, or ensure that the transfer/transferFrom return value is checked.

### locations
- solidity/tmp/test_reentrancy_transfer.sol#L47-L50
- solidity/tmp/test_reentrancy_transfer.sol#L47-L50
- solidity/tmp/test_reentrancy_transfer.sol#L57-L62
- solidity/tmp/test_reentrancy_transfer.sol#L57-L62

### severity
Medium

### category
unchecked-transfer

### confidence
Medium

## [Medium] Unsafe use of `transfer()/transferFrom()` with IERC20

### description

Some tokens do not implement the ERC20 standard properly but are still accepted by most code 
that accepts ERC20 tokens. For example Tether (USDT)'s `transfer()` and `transferFrom()` functions 
on L1 do not return booleans as the specification requires, and instead have no return value. 
When these sorts of tokens are cast to IERC20, their [function signatures](https://medium.com/coinmonks/missing-return-value-bug-at-least-130-tokens-affected-d67bf08521ca) 
do not match and therefore the calls made, revert.


**There are `4` instances of this issue:**

- [token.transfer(to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L48) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [token.transferFrom(address(this),to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L49) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [token.transfer(to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L59) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [token.transferFrom(address(this),to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L60) should be replaced by `safeTransfer()/safeTransferFrom()`.


### recommendation

Use [OpenZeppelin’s SafeERC20](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol) 
`safeTransfer()/safeTransferFrom()` instead of `transfer()/transferFrom()`


### locations
- solidity/tmp/test_reentrancy_transfer.sol#L48
- solidity/tmp/test_reentrancy_transfer.sol#L49
- solidity/tmp/test_reentrancy_transfer.sol#L59
- solidity/tmp/test_reentrancy_transfer.sol#L60

### severity
Medium

### category
unsafe-transfer

### confidence
High

## [Medium] Void function

### description
Detect the call to a function that is not implemented

**There is `1` instance of this issue:**

- function:[SafeERC20._callOptionalReturn(IERC20,bytes)](solidity/tmp/test_reentrancy_transfer.sol#L25)is empty 

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
- solidity/tmp/test_reentrancy_transfer.sol#L25

### severity
Medium

### category
void-function

### confidence
High

## [Low] Functions calling contracts/addresses with transfer hooks are missing reentrancy guards

### description

Even if the function follows the best practice of check-effects-interaction, 
not using a reentrancy guard when there may be transfer hooks will open the 
users of this protocol up to 
[read-only reentrancies](https://chainsecurity.com/curve-lp-oracle-manipulation-post-mortem/) 
with no way to protect against it, except by block-listing the whole protocol.


**There are `4` instances of this issue:**

- [token.transfer(to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L48) should use Reentrancy-Guard.

- [token.transferFrom(address(this),to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L49) should use Reentrancy-Guard.

- [token.safeTransfer(to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L53) should use Reentrancy-Guard.

- [token.safeTransferFrom(address(this),to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L54) should use Reentrancy-Guard.


### recommendation

Using [Reentrancy-Guard](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/security/ReentrancyGuard.sol#L50C5-L62) 
when calling contracts/addresses with transfer hooks.


### locations
- solidity/tmp/test_reentrancy_transfer.sol#L48
- solidity/tmp/test_reentrancy_transfer.sol#L49
- solidity/tmp/test_reentrancy_transfer.sol#L53
- solidity/tmp/test_reentrancy_transfer.sol#L54

### severity
Low

### category
reentrancy-transfer

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

## [Optimization] Cache state variables instead of rereading

### description

The instances below point to the second+ access of a state variable within a function. Caching of a state variable replaces each Gwarmaccess (**100 gas**) with a much cheaper stack read. Other less obvious fixes/optimizations include having local memory caches of state variable structs, or having local caches of state variable contracts/addresses.

More detail see [this.](https://gist.github.com/0xxfu/af8f63ccbf36af9d067ed6eff9ff7129)


**There are `4` instances of this issue:**

- [ReentrancyTransfer.token](solidity/tmp/test_reentrancy_transfer.sol#L42) should be cached with local memory-based variable in [ReentrancyTransfer.good1(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L64-L69), It is called more than once:
	- [afterBalance = token.balanceOf(to)](solidity/tmp/test_reentrancy_transfer.sol#L68)
	- [beforeBalance = token.balanceOf(to)](solidity/tmp/test_reentrancy_transfer.sol#L65)
	- [token.safeTransferFrom(address(this),to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L67)
	- [token.safeTransfer(to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L66)

- [ReentrancyTransfer.token](solidity/tmp/test_reentrancy_transfer.sol#L42) should be cached with local memory-based variable in [ReentrancyTransfer.good0(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L57-L62), It is called more than once:
	- [token.transferFrom(address(this),to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L60)
	- [token.transfer(to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L59)
	- [afterBalance = token.balanceOf(to)](solidity/tmp/test_reentrancy_transfer.sol#L61)
	- [beforeBalance = token.balanceOf(to)](solidity/tmp/test_reentrancy_transfer.sol#L58)

- [ReentrancyTransfer.token](solidity/tmp/test_reentrancy_transfer.sol#L42) should be cached with local memory-based variable in [ReentrancyTransfer.bad1(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L52-L55), It is called more than once:
	- [token.safeTransferFrom(address(this),to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L54)
	- [token.safeTransfer(to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L53)

- [ReentrancyTransfer.token](solidity/tmp/test_reentrancy_transfer.sol#L42) should be cached with local memory-based variable in [ReentrancyTransfer.bad0(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L47-L50), It is called more than once:
	- [token.transferFrom(address(this),to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L49)
	- [token.transfer(to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L48)


### recommendation

Cache storage-based state variables in local memory-based variables appropriately to convert SLOADs to MLOADs and reduce gas consumption from 100 units to 3 units. than once for a function


### locations
- solidity/tmp/test_reentrancy_transfer.sol#L42
- solidity/tmp/test_reentrancy_transfer.sol#L42
- solidity/tmp/test_reentrancy_transfer.sol#L42
- solidity/tmp/test_reentrancy_transfer.sol#L42

### severity
Optimization

### category
reread-state-variables

### confidence
High

## [Optimization] Remove unused parameter variables

### description

Unused parameters variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 



**There is `1` instance of this issue:**

- The param variables in [SafeERC20._callOptionalReturn(IERC20,bytes)](solidity/tmp/test_reentrancy_transfer.sol#L25) are unused.
	- [SafeERC20._callOptionalReturn(IERC20,bytes).token](solidity/tmp/test_reentrancy_transfer.sol#L25)
	- [SafeERC20._callOptionalReturn(IERC20,bytes).data](solidity/tmp/test_reentrancy_transfer.sol#L25)


### recommendation

Remove the unused parameter variables.


### locations
- solidity/tmp/test_reentrancy_transfer.sol#L25

### severity
Optimization

### category
unused-parameter

### confidence
High

## [Optimization] Remove unused local variables

### description

Unused local variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 


**There are `2` instances of this issue:**

- The local variables in [ReentrancyTransfer.good0(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L57-L62) are unused.
	- [ReentrancyTransfer.good0(address,uint256).afterBalance](solidity/tmp/test_reentrancy_transfer.sol#L61)
	- [ReentrancyTransfer.good0(address,uint256).beforeBalance](solidity/tmp/test_reentrancy_transfer.sol#L58)

- The local variables in [ReentrancyTransfer.good1(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L64-L69) are unused.
	- [ReentrancyTransfer.good1(address,uint256).beforeBalance](solidity/tmp/test_reentrancy_transfer.sol#L65)
	- [ReentrancyTransfer.good1(address,uint256).afterBalance](solidity/tmp/test_reentrancy_transfer.sol#L68)


### recommendation

Remove the unused local variables.


### locations
- solidity/tmp/test_reentrancy_transfer.sol#L57-L62
- solidity/tmp/test_reentrancy_transfer.sol#L64-L69

### severity
Optimization

### category
unused-local-var

### confidence
High

## [Optimization] Amounts should be checked for `0` before calling a `transfer`

### description

According to the fact that EIP-20 [states](https://github.com/ethereum/EIPs/blob/46b9b698815abbfa628cd1097311deee77dd45c5/EIPS/eip-20.md?plain=1#L116) that zero-valued transfers must be accepted.

Checking non-zero transfer values can avoid an expensive external call and save gas.
While this is done at some places, it’s not consistently done in the solution.


**There are `8` instances of this issue:**

- Adding a non-zero-value check for [token.transfer(to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L48) at the beginning of [ReentrancyTransfer.bad0(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L47-L50)

- Adding a non-zero-value check for [token.transferFrom(address(this),to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L49) at the beginning of [ReentrancyTransfer.bad0(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L47-L50)

- Adding a non-zero-value check for [token.safeTransfer(to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L53) at the beginning of [ReentrancyTransfer.bad1(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L52-L55)

- Adding a non-zero-value check for [token.safeTransferFrom(address(this),to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L54) at the beginning of [ReentrancyTransfer.bad1(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L52-L55)

- Adding a non-zero-value check for [token.transfer(to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L59) at the beginning of [ReentrancyTransfer.good0(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L57-L62)

- Adding a non-zero-value check for [token.transferFrom(address(this),to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L60) at the beginning of [ReentrancyTransfer.good0(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L57-L62)

- Adding a non-zero-value check for [token.safeTransfer(to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L66) at the beginning of [ReentrancyTransfer.good1(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L64-L69)

- Adding a non-zero-value check for [token.safeTransferFrom(address(this),to,amount)](solidity/tmp/test_reentrancy_transfer.sol#L67) at the beginning of [ReentrancyTransfer.good1(address,uint256)](solidity/tmp/test_reentrancy_transfer.sol#L64-L69)


### recommendation

Consider adding a non-zero-value check at the beginning of function.


### locations
- solidity/tmp/test_reentrancy_transfer.sol#L48
- solidity/tmp/test_reentrancy_transfer.sol#L49
- solidity/tmp/test_reentrancy_transfer.sol#L53
- solidity/tmp/test_reentrancy_transfer.sol#L54
- solidity/tmp/test_reentrancy_transfer.sol#L59
- solidity/tmp/test_reentrancy_transfer.sol#L60
- solidity/tmp/test_reentrancy_transfer.sol#L66
- solidity/tmp/test_reentrancy_transfer.sol#L67

### severity
Optimization

### category
zero-check-with-transfer

### confidence
High

## [Optimization] Empty blocks should be removed or emit something

### description

The code should be refactored such that they no longer exist, or the block should do 
something useful, such as emitting an event or reverting. 
If the contract is meant to be extended, the contract should be `abstract` and the function 
signatures be added without any default implementation.


**There is `1` instance of this issue:**

- [SafeERC20._callOptionalReturn(IERC20,bytes)](solidity/tmp/test_reentrancy_transfer.sol#L25) should removed or do something


### recommendation

Empty blocks should emit an event, or revert. 
If not, they can simply be removed to save gas upon deployment. 
This is valid for `receive()` functions, but also `constructors()`


### locations
- solidity/tmp/test_reentrancy_transfer.sol#L25

### severity
Optimization

### category
empty-block

### confidence
High

## [Optimization] State variables that could be declared constant

### description
State variables that are not updated following deployment should be declared constant to save gas.

**There is `1` instance of this issue:**

- [ReentrancyTransfer.token](solidity/tmp/test_reentrancy_transfer.sol#L42) should be constant 


### recommendation
Add the `constant` attribute to state variables that never change.

### locations
- solidity/tmp/test_reentrancy_transfer.sol#L42

### severity
Optimization

### category
constable-states

### confidence
High
