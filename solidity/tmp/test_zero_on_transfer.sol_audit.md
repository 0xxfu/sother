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
| [L-0] | Functions calling contracts/addresses with transfer hooks are missing reentrancy guards | 12 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Using custom errors replace `require` or `assert` | 2 |
| [G-1] | Cache state variables instead of rereading | 6 |
| [G-2] | Remove unused parameter variables | 1 |
| [G-3] | Remove unused local variables | 4 |
| [G-4] | Amounts should be checked for `0` before calling a `transfer` | 4 |
| [G-5] | Empty blocks should be removed or emit something | 1 |
| [G-6] | State variables that could be declared constant | 1 |



## [High] Uninitialized state variables

### description
Uninitialized state variables.

**There is `1` instance of this issue:**

- [ZeroOnTransfer.token](solidity/tmp/test_zero_on_transfer.sol#L42) is never initialized. It is used in:
	- [ZeroOnTransfer.bad0(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L44-L47)
	- [ZeroOnTransfer.bad1(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L49-L52)
	- [ZeroOnTransfer.good0(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L54-L62)
	- [ZeroOnTransfer.good1(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L64-L72)
	- [ZeroOnTransfer.good2(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L74-L80)
	- [ZeroOnTransfer.good3(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L82-L88)

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
- solidity/tmp/test_zero_on_transfer.sol#L42

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

- state variable: [ZeroOnTransfer.token](solidity/tmp/test_zero_on_transfer.sol#L42) not initialized and not written in contract but be used in contract

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
- solidity/tmp/test_zero_on_transfer.sol#L42

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

- [ZeroOnTransfer.bad0(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L44-L47) ignores return value by [token.transferFrom(address(this),to,amount)](solidity/tmp/test_zero_on_transfer.sol#L46)

- [ZeroOnTransfer.bad0(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L44-L47) ignores return value by [token.transfer(to,amount)](solidity/tmp/test_zero_on_transfer.sol#L45)

- [ZeroOnTransfer.good0(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L54-L62) ignores return value by [token.transferFrom(address(this),to,amount)](solidity/tmp/test_zero_on_transfer.sol#L60)

- [ZeroOnTransfer.good0(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L54-L62) ignores return value by [token.transfer(to,amount)](solidity/tmp/test_zero_on_transfer.sol#L59)

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
- solidity/tmp/test_zero_on_transfer.sol#L44-L47
- solidity/tmp/test_zero_on_transfer.sol#L44-L47
- solidity/tmp/test_zero_on_transfer.sol#L54-L62
- solidity/tmp/test_zero_on_transfer.sol#L54-L62

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

- [token.transfer(to,amount)](solidity/tmp/test_zero_on_transfer.sol#L45) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [token.transferFrom(address(this),to,amount)](solidity/tmp/test_zero_on_transfer.sol#L46) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [token.transfer(to,amount)](solidity/tmp/test_zero_on_transfer.sol#L59) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [token.transferFrom(address(this),to,amount)](solidity/tmp/test_zero_on_transfer.sol#L60) should be replaced by `safeTransfer()/safeTransferFrom()`.


### recommendation

Use [OpenZeppelin’s SafeERC20](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol) 
`safeTransfer()/safeTransferFrom()` instead of `transfer()/transferFrom()`


### locations
- solidity/tmp/test_zero_on_transfer.sol#L45
- solidity/tmp/test_zero_on_transfer.sol#L46
- solidity/tmp/test_zero_on_transfer.sol#L59
- solidity/tmp/test_zero_on_transfer.sol#L60

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

- function:[SafeERC20._callOptionalReturn(IERC20,bytes)](solidity/tmp/test_zero_on_transfer.sol#L25)is empty 

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
- solidity/tmp/test_zero_on_transfer.sol#L25

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


**There are `12` instances of this issue:**

- [token.transfer(to,amount)](solidity/tmp/test_zero_on_transfer.sol#L45) should use Reentrancy-Guard.

- [token.transferFrom(address(this),to,amount)](solidity/tmp/test_zero_on_transfer.sol#L46) should use Reentrancy-Guard.

- [token.safeTransfer(to,amount)](solidity/tmp/test_zero_on_transfer.sol#L50) should use Reentrancy-Guard.

- [token.safeTransferFrom(address(this),to,amount)](solidity/tmp/test_zero_on_transfer.sol#L51) should use Reentrancy-Guard.

- [token.transfer(to,amount)](solidity/tmp/test_zero_on_transfer.sol#L59) should use Reentrancy-Guard.

- [token.transferFrom(address(this),to,amount)](solidity/tmp/test_zero_on_transfer.sol#L60) should use Reentrancy-Guard.

- [token.safeTransfer(to,amount)](solidity/tmp/test_zero_on_transfer.sol#L69) should use Reentrancy-Guard.

- [token.safeTransferFrom(address(this),to,amount)](solidity/tmp/test_zero_on_transfer.sol#L70) should use Reentrancy-Guard.

- [token.safeTransfer(to,amount)](solidity/tmp/test_zero_on_transfer.sol#L77) should use Reentrancy-Guard.

- [token.safeTransferFrom(address(this),to,amount)](solidity/tmp/test_zero_on_transfer.sol#L78) should use Reentrancy-Guard.

- [token.safeTransfer(to,amount)](solidity/tmp/test_zero_on_transfer.sol#L85) should use Reentrancy-Guard.

- [token.safeTransferFrom(address(this),to,amount)](solidity/tmp/test_zero_on_transfer.sol#L86) should use Reentrancy-Guard.


### recommendation

Using [Reentrancy-Guard](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/security/ReentrancyGuard.sol#L50C5-L62) 
when calling contracts/addresses with transfer hooks.


### locations
- solidity/tmp/test_zero_on_transfer.sol#L45
- solidity/tmp/test_zero_on_transfer.sol#L46
- solidity/tmp/test_zero_on_transfer.sol#L50
- solidity/tmp/test_zero_on_transfer.sol#L51
- solidity/tmp/test_zero_on_transfer.sol#L59
- solidity/tmp/test_zero_on_transfer.sol#L60
- solidity/tmp/test_zero_on_transfer.sol#L69
- solidity/tmp/test_zero_on_transfer.sol#L70
- solidity/tmp/test_zero_on_transfer.sol#L77
- solidity/tmp/test_zero_on_transfer.sol#L78
- solidity/tmp/test_zero_on_transfer.sol#L85
- solidity/tmp/test_zero_on_transfer.sol#L86

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

## [Optimization] Using custom errors replace `require` or `assert`

### description

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `2` instances of this issue:**

- [require(bool,string)(amount == 0,"error")](solidity/tmp/test_zero_on_transfer.sol#L75) should use custom error to save gas.

- [require(bool,string)(amount <= 0,"error")](solidity/tmp/test_zero_on_transfer.sol#L83) should use custom error to save gas.


### recommendation

Using custom errors replace `require` or `assert`.


### locations
- solidity/tmp/test_zero_on_transfer.sol#L75
- solidity/tmp/test_zero_on_transfer.sol#L83

### severity
Optimization

### category
use-custom-error

### confidence
High

## [Optimization] Cache state variables instead of rereading

### description

The instances below point to the second+ access of a state variable within a function. Caching of a state variable replaces each Gwarmaccess (**100 gas**) with a much cheaper stack read. Other less obvious fixes/optimizations include having local memory caches of state variable structs, or having local caches of state variable contracts/addresses.

More detail see [this.](https://gist.github.com/0xxfu/af8f63ccbf36af9d067ed6eff9ff7129)


**There are `6` instances of this issue:**

- [ZeroOnTransfer.token](solidity/tmp/test_zero_on_transfer.sol#L42) should be cached with local memory-based variable in [ZeroOnTransfer.good1(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L64-L72), It is called more than once:
	- [token.safeTransferFrom(address(this),to,amount)](solidity/tmp/test_zero_on_transfer.sol#L70)
	- [token.safeTransfer(to,amount)](solidity/tmp/test_zero_on_transfer.sol#L69)
	- [afterBalance = token.balanceOf(to)](solidity/tmp/test_zero_on_transfer.sol#L71)
	- [beforeBalance = token.balanceOf(to)](solidity/tmp/test_zero_on_transfer.sol#L68)

- [ZeroOnTransfer.token](solidity/tmp/test_zero_on_transfer.sol#L42) should be cached with local memory-based variable in [ZeroOnTransfer.good0(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L54-L62), It is called more than once:
	- [beforeBalance = token.balanceOf(to)](solidity/tmp/test_zero_on_transfer.sol#L58)
	- [token.transferFrom(address(this),to,amount)](solidity/tmp/test_zero_on_transfer.sol#L60)
	- [token.transfer(to,amount)](solidity/tmp/test_zero_on_transfer.sol#L59)
	- [afterBalance = token.balanceOf(to)](solidity/tmp/test_zero_on_transfer.sol#L61)

- [ZeroOnTransfer.token](solidity/tmp/test_zero_on_transfer.sol#L42) should be cached with local memory-based variable in [ZeroOnTransfer.bad0(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L44-L47), It is called more than once:
	- [token.transferFrom(address(this),to,amount)](solidity/tmp/test_zero_on_transfer.sol#L46)
	- [token.transfer(to,amount)](solidity/tmp/test_zero_on_transfer.sol#L45)

- [ZeroOnTransfer.token](solidity/tmp/test_zero_on_transfer.sol#L42) should be cached with local memory-based variable in [ZeroOnTransfer.good3(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L82-L88), It is called more than once:
	- [token.safeTransfer(to,amount)](solidity/tmp/test_zero_on_transfer.sol#L85)
	- [afterBalance = token.balanceOf(to)](solidity/tmp/test_zero_on_transfer.sol#L87)
	- [token.safeTransferFrom(address(this),to,amount)](solidity/tmp/test_zero_on_transfer.sol#L86)
	- [beforeBalance = token.balanceOf(to)](solidity/tmp/test_zero_on_transfer.sol#L84)

- [ZeroOnTransfer.token](solidity/tmp/test_zero_on_transfer.sol#L42) should be cached with local memory-based variable in [ZeroOnTransfer.good2(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L74-L80), It is called more than once:
	- [token.safeTransferFrom(address(this),to,amount)](solidity/tmp/test_zero_on_transfer.sol#L78)
	- [token.safeTransfer(to,amount)](solidity/tmp/test_zero_on_transfer.sol#L77)
	- [afterBalance = token.balanceOf(to)](solidity/tmp/test_zero_on_transfer.sol#L79)
	- [beforeBalance = token.balanceOf(to)](solidity/tmp/test_zero_on_transfer.sol#L76)

- [ZeroOnTransfer.token](solidity/tmp/test_zero_on_transfer.sol#L42) should be cached with local memory-based variable in [ZeroOnTransfer.bad1(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L49-L52), It is called more than once:
	- [token.safeTransfer(to,amount)](solidity/tmp/test_zero_on_transfer.sol#L50)
	- [token.safeTransferFrom(address(this),to,amount)](solidity/tmp/test_zero_on_transfer.sol#L51)


### recommendation

Cache storage-based state variables in local memory-based variables appropriately to convert SLOADs to MLOADs and reduce gas consumption from 100 units to 3 units. than once for a function


### locations
- solidity/tmp/test_zero_on_transfer.sol#L42
- solidity/tmp/test_zero_on_transfer.sol#L42
- solidity/tmp/test_zero_on_transfer.sol#L42
- solidity/tmp/test_zero_on_transfer.sol#L42
- solidity/tmp/test_zero_on_transfer.sol#L42
- solidity/tmp/test_zero_on_transfer.sol#L42

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

- The param variables in [SafeERC20._callOptionalReturn(IERC20,bytes)](solidity/tmp/test_zero_on_transfer.sol#L25) are unused.
	- [SafeERC20._callOptionalReturn(IERC20,bytes).token](solidity/tmp/test_zero_on_transfer.sol#L25)
	- [SafeERC20._callOptionalReturn(IERC20,bytes).data](solidity/tmp/test_zero_on_transfer.sol#L25)


### recommendation

Remove the unused parameter variables.


### locations
- solidity/tmp/test_zero_on_transfer.sol#L25

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


**There are `4` instances of this issue:**

- The local variables in [ZeroOnTransfer.good0(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L54-L62) are unused.
	- [ZeroOnTransfer.good0(address,uint256).beforeBalance](solidity/tmp/test_zero_on_transfer.sol#L58)
	- [ZeroOnTransfer.good0(address,uint256).afterBalance](solidity/tmp/test_zero_on_transfer.sol#L61)

- The local variables in [ZeroOnTransfer.good1(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L64-L72) are unused.
	- [ZeroOnTransfer.good1(address,uint256).afterBalance](solidity/tmp/test_zero_on_transfer.sol#L71)
	- [ZeroOnTransfer.good1(address,uint256).beforeBalance](solidity/tmp/test_zero_on_transfer.sol#L68)

- The local variables in [ZeroOnTransfer.good2(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L74-L80) are unused.
	- [ZeroOnTransfer.good2(address,uint256).afterBalance](solidity/tmp/test_zero_on_transfer.sol#L79)
	- [ZeroOnTransfer.good2(address,uint256).beforeBalance](solidity/tmp/test_zero_on_transfer.sol#L76)

- The local variables in [ZeroOnTransfer.good3(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L82-L88) are unused.
	- [ZeroOnTransfer.good3(address,uint256).afterBalance](solidity/tmp/test_zero_on_transfer.sol#L87)
	- [ZeroOnTransfer.good3(address,uint256).beforeBalance](solidity/tmp/test_zero_on_transfer.sol#L84)


### recommendation

Remove the unused local variables.


### locations
- solidity/tmp/test_zero_on_transfer.sol#L54-L62
- solidity/tmp/test_zero_on_transfer.sol#L64-L72
- solidity/tmp/test_zero_on_transfer.sol#L74-L80
- solidity/tmp/test_zero_on_transfer.sol#L82-L88

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


**There are `4` instances of this issue:**

- Adding a non-zero-value check for [token.transfer(to,amount)](solidity/tmp/test_zero_on_transfer.sol#L45) at the beginning of [ZeroOnTransfer.bad0(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L44-L47)

- Adding a non-zero-value check for [token.transferFrom(address(this),to,amount)](solidity/tmp/test_zero_on_transfer.sol#L46) at the beginning of [ZeroOnTransfer.bad0(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L44-L47)

- Adding a non-zero-value check for [token.safeTransfer(to,amount)](solidity/tmp/test_zero_on_transfer.sol#L50) at the beginning of [ZeroOnTransfer.bad1(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L49-L52)

- Adding a non-zero-value check for [token.safeTransferFrom(address(this),to,amount)](solidity/tmp/test_zero_on_transfer.sol#L51) at the beginning of [ZeroOnTransfer.bad1(address,uint256)](solidity/tmp/test_zero_on_transfer.sol#L49-L52)


### recommendation

Consider adding a non-zero-value check at the beginning of function.


### locations
- solidity/tmp/test_zero_on_transfer.sol#L45
- solidity/tmp/test_zero_on_transfer.sol#L46
- solidity/tmp/test_zero_on_transfer.sol#L50
- solidity/tmp/test_zero_on_transfer.sol#L51

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

- [SafeERC20._callOptionalReturn(IERC20,bytes)](solidity/tmp/test_zero_on_transfer.sol#L25) should removed or do something


### recommendation

Empty blocks should emit an event, or revert. 
If not, they can simply be removed to save gas upon deployment. 
This is valid for `receive()` functions, but also `constructors()`


### locations
- solidity/tmp/test_zero_on_transfer.sol#L25

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

- [ZeroOnTransfer.token](solidity/tmp/test_zero_on_transfer.sol#L42) should be constant 


### recommendation
Add the `constant` attribute to state variables that never change.

### locations
- solidity/tmp/test_zero_on_transfer.sol#L42

### severity
Optimization

### category
constable-states

### confidence
High
