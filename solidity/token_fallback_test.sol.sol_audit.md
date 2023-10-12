## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Return values of `transfer()/transferFrom()` not checked | 1 |
| [M-1] | Unsafe use of `transfer()/transferFrom()` with IERC20 | 1 |
| [M-2] | Incompatibility with transfer-on-fee or deflationary tokens | 1 |
| [M-3] | The owner is a single point of failure and a centralization risk | 1 |
| [M-4] | Integer Overflow and Underflow | 4 |
| [M-5] | Void function | 2 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Lack of a double-step `transferOwnership()` pattern | 1 |
| [L-1] | Unsafe to use floating pragma | 5 |
| [L-2] | Functions calling contracts/addresses with transfer hooks are missing reentrancy guards | 1 |
| [L-3] | Missing Event Setter | 6 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 7 |
| [N-1] | Too many digits | 1 |
| [N-2] | Different pragma directives are used | 1 |
| [N-3] | Low-level calls | 1 |
| [N-4] | Conformance to Solidity naming conventions | 1 |
| [N-5] | Unnecessary Public Function Modifier | 14 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Should use latest solidity version `0.8.21` for gas reduction and improved security. | 5 |
| [G-1] | `<x> += <y>` costs more gas than `<x> = <x> + <y>` for state variables | 3 |
| [G-2] | `internal` functions only called once can be inlined to save gas | 1 |
| [G-3] | Using custom errors replace `require` or `assert` | 9 |
| [G-4] | Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead | 2 |
| [G-5] | Remove unused parameter variables | 2 |
| [G-6] | Remove unused local variables | 1 |
| [G-7] | The result of function calls should be cached rather than re-calling the function | 3 |
| [G-8] | Dead-code: functions not used should be removed to save deployment gas | 1 |
| [G-9] | Use indexed events for value types as they are less costly compared to non-indexed ones | 2 |
| [G-10] | Amounts should be checked for `0` before calling a `transfer` | 1 |
| [G-11] | Use assembly to check for `address(0)` | 5 |
| [G-12] | Setting the constructor to `payable` | 3 |
| [G-13] | Functions guaranteed to revert when called by normal users can be marked `payable` | 2 |
| [G-14] | Shortening revert strings to fit in 32 `bytes` | 7 |
| [G-15] | Use `assembly` to write address storage values | 1 |
| [G-16] | Empty blocks should be removed or emit something | 2 |
| [G-17] | Use `selfbalance()` instead of `address(this).balance` | 2 |
| [G-18] | Use `delete` to Clear Variables | 1 |
| [G-19] | State variables that could be declared constant | 1 |
| [G-20] | State variables that could be declared constant | 1 |



## [Medium] Return values of `transfer()/transferFrom()` not checked

### description

Not all `IERC20` implementations `revert()` when there's a failure in `transfer()`/`transferFrom()`. The function signature has a `boolean` return value and they indicate errors that way instead. By not checking the return value, operations that should have marked as failed, may potentially go through without actually making a payment.


**There is `1` instance of this issue:**

- [AmazoniumToken.purgeBadToken(IERC20)](solidity/token_fallback_test.sol.sol#L219-L222) ignores return value by [badToken.transfer(distAddr,BadTokenBalance)](solidity/token_fallback_test.sol.sol#L221)

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
- solidity/token_fallback_test.sol.sol#L219-L222

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


**There is `1` instance of this issue:**

- [badToken.transfer(distAddr,BadTokenBalance)](solidity/token_fallback_test.sol.sol#L221) should be replaced by `safeTransfer()/safeTransferFrom()`.


### recommendation

Use [OpenZeppelin’s SafeERC20](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol) 
`safeTransfer()/safeTransferFrom()` instead of `transfer()/transferFrom()`


### locations
- solidity/token_fallback_test.sol.sol#L221

### severity
Medium

### category
unsafe-transfer

### confidence
High

## [Medium] Incompatibility with transfer-on-fee or deflationary tokens

### description

Some ERC20 tokens make modifications to the standard implementations of
their ERC20’s `transfer` or `balanceOf` functions.
One type of such token is deflationary tokens that charge a fee on every
`transfer()` and `transferFrom()`.
The protocol does not have incompatibility with fee-on-transfer tokens.

Note that there has been a real-world exploit related to this with 
[Balancer pool and STA deflationary tokens](https://medium.com/1inch-network/balancer-hack-2020-a8f7131c980e).


**There is `1` instance of this issue:**

- [badToken.transfer(distAddr,BadTokenBalance)](solidity/token_fallback_test.sol.sol#L221) with fee on transfer are not supported.

#### Exploit scenario

i.e. Fee-on-transfer scenario:
1. Contract calls transfer from contractA 100 tokens to current contract
2. Current contract thinks it received 100 tokens
3. It updates balances to increase +100 tokens
4. While actually contract received only 90 tokens
5. That breaks whole math for given token


### recommendation

1. Consider comparing before and after balance to get the actual transferred amount.
2. Alternatively, disallow tokens with fee-on-transfer mechanics to be added as tokens.


### locations
- solidity/token_fallback_test.sol.sol#L221

### severity
Medium

### category
fee-on-transfer

### confidence
Medium

## [Medium] The owner is a single point of failure and a centralization risk

### description

Having a single EOA as the only owner of contracts is a large centralization risk and a single point of failure. A single private key may be taken in a hack, or the sole holder of the key may become unable to retrieve the key when necessary.

There are several privileged entities that have access to sensitive operations as follows.


**There is `1` instance of this issue:**

- The role [Ownable.onlyOwner()](solidity/token_fallback_test.sol.sol#L194-L196) is a single point of failure and a centralization risk. and have access to sensitive operations as follows:
	- [AmazoniumToken.Distribute()](solidity/token_fallback_test.sol.sol#L212-L217)
	- [AmazoniumToken.purgeBadToken(IERC20)](solidity/token_fallback_test.sol.sol#L219-L222)


### recommendation

Add a time lock to critical functions. Admin-only functions that change critical parameters should emit events and have timelocks.
Events allow capturing the changed parameters so that off-chain tools/interfaces can register such changes with timelocks that allow users to evaluate them and consider if they would like to engage/exit based on how they perceive the changes as affecting the trustworthiness of the protocol or profitability of the implemented financial services.

Allow only multi-signature wallets to call the function to reduce the likelihood of an attack.


### locations
- solidity/token_fallback_test.sol.sol#L194-L196

### severity
Medium

### category
owner-centralization

### confidence
High

## [Medium] Integer Overflow and Underflow

### description

    若不使用OpenZeppelin的SafeMath(或类似的库)检查溢出/下溢，
    如果用户/攻击者能够控制这种算术运算的整数操作数，
    可能会导致漏洞或意外行为。
    Solc v0.8.0为所有算术运算引入了默认的溢出/底溢检查。(见这里和这里)

**There are `4` instances of this issue:**

- increaseAllowance(address,uint256) has possible integer overflow/underflow:
	- [_approve(_msgSender(),spender,_allowances[_msgSender()][spender] + addedValue)](solidity/token_fallback_test.sol.sol#L108)

- _transfer(address,address,uint256) has possible integer overflow/underflow:
	- [_balances[recipient] += amount](solidity/token_fallback_test.sol.sol#L137)

- receive() has possible integer overflow/underflow:
	- [balance += msg.value](solidity/token_fallback_test.sol.sol#L225)

- fallback() has possible integer overflow/underflow:
	- [balance += msg.value](solidity/token_fallback_test.sol.sol#L229)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/token_fallback_test.sol.sol#L108
- solidity/token_fallback_test.sol.sol#L137
- solidity/token_fallback_test.sol.sol#L225
- solidity/token_fallback_test.sol.sol#L229

### severity
Medium

### category
integer-overflow

### confidence
High

## [Medium] Void function

### description
Detect the call to a function that is not implemented

**There are `2` instances of this issue:**

- function:[ERC20._beforeTokenTransfer(address,address,uint256)](solidity/token_fallback_test.sol.sol#L168-L172)is empty 

- function:[ERC20._afterTokenTransfer(address,address,uint256)](solidity/token_fallback_test.sol.sol#L174-L178)is empty 

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
- solidity/token_fallback_test.sol.sol#L168-L172
- solidity/token_fallback_test.sol.sol#L174-L178

### severity
Medium

### category
void-function

### confidence
High

## [Low] Lack of a double-step `transferOwnership()` pattern

### description

The current ownership transfer process for all the contracts inheriting
from `Ownable` or `OwnableUpgradeable` involves the current owner calling the
[transferOwnership()](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.8/contracts/access/Ownable.sol#L69-L72) function:

```
    function transferOwnership(address newOwner) public virtual onlyOwner {
        require(newOwner != address(0), "Ownable: new owner is the zero address");
        _transferOwnership(newOwner);
    }
```
If the nominated EOA account is not a valid account, it is entirely possible
that the owner may accidentally transfer ownership to an uncontrolled
account, losing the access to all functions with the `onlyOwner` modifier.



**There is `1` instance of this issue:**

- [AmazoniumToken](solidity/token_fallback_test.sol.sol#L202-L232) does not implement a `2-Step-Process` for transferring ownership.

### recommendation

It is recommended to implement a two-step process where the owner nominates
an account and the nominated account needs to call an `acceptOwnership()`
function for the transfer of the ownership to fully succeed. This ensures
the nominated EOA account is a valid and active account. This can be
easily achieved by using OpenZeppelin’s [Ownable2Step](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.8/contracts/access/Ownable2Step.sol) contract instead of
`Ownable`:

```
abstract contract Ownable2Step is Ownable {

    /**
     * @dev Starts the ownership transfer of the contract to a new account. Replaces the pending transfer if there is one.
     * Can only be called by the current owner.
     */
    function transferOwnership(address newOwner) public virtual override onlyOwner {
        _pendingOwner = newOwner;
        emit OwnershipTransferStarted(owner(), newOwner);
    }
    
    ...

    /**
     * @dev The new owner accepts the ownership transfer.
     */
    function acceptOwnership() external {
        address sender = _msgSender();
        require(pendingOwner() == sender, "Ownable2Step: caller is not the new owner");
        _transferOwnership(sender);
    }
}
```


### locations
- solidity/token_fallback_test.sol.sol#L202-L232

### severity
Low

### category
deprecated-ownable

### confidence
High

## [Low] Unsafe to use floating pragma

### description

Contracts should be deployed with the same compiler version and flags that 
they have been tested with thoroughly. 
Locking the pragma helps to ensure that contracts do not accidentally get deployed using, 
for example, an outdated compiler version that might introduce bugs that affect the 
contract system negatively.

More detail see [SWC-103](https://swcregistry.io/docs/SWC-103).


**There are `5` instances of this issue:**

- Should lock the pragma version instead of floating pragma: [^0.8.0](solidity/token_fallback_test.sol.sol#L3). 

- Should lock the pragma version instead of floating pragma: [^0.8.0](solidity/token_fallback_test.sol.sol#L15). 

- Should lock the pragma version instead of floating pragma: [^0.8.0](solidity/token_fallback_test.sol.sol#L33). 

- Should lock the pragma version instead of floating pragma: [^0.8.0](solidity/token_fallback_test.sol.sol#L42). 

- Should lock the pragma version instead of floating pragma: [^0.8.0](solidity/token_fallback_test.sol.sol#L181). 


### recommendation

Lock the pragma version and also consider known bugs (https://github.com/ethereum/solidity/releases) 
for the compiler version that is chosen.


### locations
- solidity/token_fallback_test.sol.sol#L3
- solidity/token_fallback_test.sol.sol#L15
- solidity/token_fallback_test.sol.sol#L33
- solidity/token_fallback_test.sol.sol#L42
- solidity/token_fallback_test.sol.sol#L181

### severity
Low

### category
unsafe-floating-pragma

### confidence
High

## [Low] Functions calling contracts/addresses with transfer hooks are missing reentrancy guards

### description

Even if the function follows the best practice of check-effects-interaction, 
not using a reentrancy guard when there may be transfer hooks will open the 
users of this protocol up to 
[read-only reentrancies](https://chainsecurity.com/curve-lp-oracle-manipulation-post-mortem/) 
with no way to protect against it, except by block-listing the whole protocol.


**There is `1` instance of this issue:**

- [badToken.transfer(distAddr,BadTokenBalance)](solidity/token_fallback_test.sol.sol#L221) should use Reentrancy-Guard.


### recommendation

Using [Reentrancy-Guard](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/security/ReentrancyGuard.sol#L50C5-L62) 
when calling contracts/addresses with transfer hooks.


### locations
- solidity/token_fallback_test.sol.sol#L221

### severity
Low

### category
reentrancy-transfer

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `6` instances of this issue:**

- Setter function [AmazoniumToken.slitherConstructorVariables()](solidity/token_fallback_test.sol.sol#L202-L232) does not emit an event

- Setter function [AmazoniumToken.constructor()](solidity/token_fallback_test.sol.sol#L207-L211) does not emit an event

- Setter function [AmazoniumToken.Distribute()](solidity/token_fallback_test.sol.sol#L212-L217) does not emit an event

- Setter function [AmazoniumToken.purgeBadToken(IERC20)](solidity/token_fallback_test.sol.sol#L219-L222) does not emit an event

- Setter function [AmazoniumToken.receive()](solidity/token_fallback_test.sol.sol#L224-L226) does not emit an event

- Setter function [AmazoniumToken.fallback()](solidity/token_fallback_test.sol.sol#L228-L230) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/token_fallback_test.sol.sol#L202-L232
- solidity/token_fallback_test.sol.sol#L207-L211
- solidity/token_fallback_test.sol.sol#L212-L217
- solidity/token_fallback_test.sol.sol#L219-L222
- solidity/token_fallback_test.sol.sol#L224-L226
- solidity/token_fallback_test.sol.sol#L228-L230

### severity
Low

### category
pess-event-setter

### confidence
Medium

## [Informational] Incorrect versions of Solidity

### description

`solc` frequently releases new compiler versions. Using an old version prevents access to new Solidity security checks.
We also recommend avoiding complex `pragma` statement.

**There are `7` instances of this issue:**

- Pragma version[^0.8.0](solidity/token_fallback_test.sol.sol#L3) allows old versions

- Pragma version[^0.8.0](solidity/token_fallback_test.sol.sol#L15) allows old versions

- Pragma version[^0.8.0](solidity/token_fallback_test.sol.sol#L33) allows old versions

- Pragma version[^0.8.0](solidity/token_fallback_test.sol.sol#L42) allows old versions

- Pragma version[^0.8.0](solidity/token_fallback_test.sol.sol#L181) allows old versions

- Pragma version[>=0.4.22<0.9.0](solidity/token_fallback_test.sol.sol#L200) is too complex

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
- solidity/token_fallback_test.sol.sol#L3
- solidity/token_fallback_test.sol.sol#L15
- solidity/token_fallback_test.sol.sol#L33
- solidity/token_fallback_test.sol.sol#L42
- solidity/token_fallback_test.sol.sol#L181
- solidity/token_fallback_test.sol.sol#L200
- 

### severity
Informational

### category
solc-version

### confidence
High

## [Informational] Too many digits

### description

Literals with many digits are difficult to read and review.


**There is `1` instance of this issue:**

- [AmazoniumToken.constructor()](solidity/token_fallback_test.sol.sol#L207-L211) uses literals with too many digits:
	- [_mint(address(this),9000000 * (10 ** uint256(decimals())))](solidity/token_fallback_test.sol.sol#L208)

#### Exploit scenario

```solidity
contract MyContract{
    uint 1_ether = 10000000000000000000; 
}
```

While `1_ether` looks like `1 ether`, it is `10 ether`. As a result, it's likely to be used incorrectly.


### recommendation

Use:
- [Ether suffix](https://solidity.readthedocs.io/en/latest/units-and-global-variables.html#ether-units),
- [Time suffix](https://solidity.readthedocs.io/en/latest/units-and-global-variables.html#time-units), or
- [The scientific notation](https://solidity.readthedocs.io/en/latest/types.html#rational-and-integer-literals)


### locations
- solidity/token_fallback_test.sol.sol#L207-L211

### severity
Informational

### category
too-many-digits

### confidence
Medium

## [Informational] Different pragma directives are used

### description
Detect whether different Solidity versions are used.

**There is `1` instance of this issue:**

- Different versions of Solidity are used:
	- Version used: ['>=0.4.22<0.9.0', '^0.8.0']
	- [>=0.4.22<0.9.0](solidity/token_fallback_test.sol.sol#L200)
	- [^0.8.0](solidity/token_fallback_test.sol.sol#L3)
	- [^0.8.0](solidity/token_fallback_test.sol.sol#L15)
	- [^0.8.0](solidity/token_fallback_test.sol.sol#L33)
	- [^0.8.0](solidity/token_fallback_test.sol.sol#L42)
	- [^0.8.0](solidity/token_fallback_test.sol.sol#L181)


### recommendation
Use one Solidity version.

### locations
- solidity/token_fallback_test.sol.sol#L200

### severity
Informational

### category
pragma

### confidence
High

## [Informational] Low-level calls

### description
The use of low-level calls is error-prone. Low-level calls do not check for [code existence](https://solidity.readthedocs.io/en/v0.4.25/control-structures.html#error-handling-assert-require-revert-and-exceptions) or call success.

**There is `1` instance of this issue:**

- Low level call in [AmazoniumToken.Distribute()](solidity/token_fallback_test.sol.sol#L212-L217):
	- [(sent,None) = address(distAddr).call{value: address(this).balance}("")](solidity/token_fallback_test.sol.sol#L214)


### recommendation
Avoid low-level calls. Check the call success. If the call is meant for a contract, check for code existence.

### locations
- solidity/token_fallback_test.sol.sol#L212-L217

### severity
Informational

### category
low-level-calls

### confidence
High

## [Informational] Conformance to Solidity naming conventions

### description

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There is `1` instance of this issue:**

- Function [AmazoniumToken.Distribute()](solidity/token_fallback_test.sol.sol#L212-L217) is not in mixedCase


### recommendation
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations
- solidity/token_fallback_test.sol.sol#L212-L217

### severity
Informational

### category
naming-convention

### confidence
High

## [Informational] Unnecessary Public Function Modifier

### description
Detect the public function which can be replaced with external

**There are `14` instances of this issue:**

- function:[ERC20.name()](solidity/token_fallback_test.sol.sol#L57-L59)is public and can be replaced with external 

- function:[ERC20.symbol()](solidity/token_fallback_test.sol.sol#L61-L63)is public and can be replaced with external 

- function:[ERC20.decimals()](solidity/token_fallback_test.sol.sol#L65-L67)is public and can be replaced with external 

- function:[ERC20.totalSupply()](solidity/token_fallback_test.sol.sol#L69-L71)is public and can be replaced with external 

- function:[ERC20.balanceOf(address)](solidity/token_fallback_test.sol.sol#L73-L75)is public and can be replaced with external 

- function:[ERC20.transfer(address,uint256)](solidity/token_fallback_test.sol.sol#L77-L80)is public and can be replaced with external 

- function:[ERC20.allowance(address,address)](solidity/token_fallback_test.sol.sol#L82-L84)is public and can be replaced with external 

- function:[ERC20.approve(address,uint256)](solidity/token_fallback_test.sol.sol#L86-L89)is public and can be replaced with external 

- function:[ERC20.transferFrom(address,address,uint256)](solidity/token_fallback_test.sol.sol#L91-L105)is public and can be replaced with external 

- function:[ERC20.increaseAllowance(address,uint256)](solidity/token_fallback_test.sol.sol#L107-L110)is public and can be replaced with external 

- function:[ERC20.decreaseAllowance(address,uint256)](solidity/token_fallback_test.sol.sol#L112-L120)is public and can be replaced with external 

- function:[Ownable.owner()](solidity/token_fallback_test.sol.sol#L190-L192)is public and can be replaced with external 

- function:[AmazoniumToken.Distribute()](solidity/token_fallback_test.sol.sol#L212-L217)is public and can be replaced with external 

- function:[AmazoniumToken.purgeBadToken(IERC20)](solidity/token_fallback_test.sol.sol#L219-L222)is public and can be replaced with external 

#### Exploit scenario

```solidity
contract A{}
contract B is A{
    constructor() public A(){}
}
```
When reading `B`'s constructor definition, we might assume that `A()` initiates the contract, but no code is executed.

### recommendation
Replace public with external

### locations
- solidity/token_fallback_test.sol.sol#L57-L59
- solidity/token_fallback_test.sol.sol#L61-L63
- solidity/token_fallback_test.sol.sol#L65-L67
- solidity/token_fallback_test.sol.sol#L69-L71
- solidity/token_fallback_test.sol.sol#L73-L75
- solidity/token_fallback_test.sol.sol#L77-L80
- solidity/token_fallback_test.sol.sol#L82-L84
- solidity/token_fallback_test.sol.sol#L86-L89
- solidity/token_fallback_test.sol.sol#L91-L105
- solidity/token_fallback_test.sol.sol#L107-L110
- solidity/token_fallback_test.sol.sol#L112-L120
- solidity/token_fallback_test.sol.sol#L190-L192
- solidity/token_fallback_test.sol.sol#L212-L217
- solidity/token_fallback_test.sol.sol#L219-L222

### severity
Informational

### category
unnecessary-public-function-modifier

### confidence
High

## [Optimization] Should use latest solidity version `0.8.21` for gas reduction and improved security.

### description

[Solidity `0.8.21`](https://soliditylang.org/blog/2023/07/19/solidity-0.8.21-release-announcement) has many optimization with compiler and bugfixes, 
please upgrade Solidity to the latest version(`0.8.21`) for gas reduction and improved security.


**There are `5` instances of this issue:**

- pragma solidity version [^0.8.0](solidity/token_fallback_test.sol.sol#L3) should upgrade to the latest version: 0.8.21
- pragma solidity version [^0.8.0](solidity/token_fallback_test.sol.sol#L15) should upgrade to the latest version: 0.8.21
- pragma solidity version [^0.8.0](solidity/token_fallback_test.sol.sol#L33) should upgrade to the latest version: 0.8.21
- pragma solidity version [^0.8.0](solidity/token_fallback_test.sol.sol#L42) should upgrade to the latest version: 0.8.21
- pragma solidity version [^0.8.0](solidity/token_fallback_test.sol.sol#L181) should upgrade to the latest version: 0.8.21

### recommendation
Upgrade solidity version to the latest version: 0.8.21

### locations
- solidity/token_fallback_test.sol.sol#L3
- solidity/token_fallback_test.sol.sol#L15
- solidity/token_fallback_test.sol.sol#L33
- solidity/token_fallback_test.sol.sol#L42
- solidity/token_fallback_test.sol.sol#L181

### severity
Optimization

### category
upgrade-to-latest

### confidence
High

## [Optimization] `<x> += <y>` costs more gas than `<x> = <x> + <y>` for state variables

### description
Using the addition operator instead of plus-equals saves **[113 gas](https://gist.github.com/0xxfu/86ae4bdd07d7db169cea110dba5a5af4)**

**There are `3` instances of this issue:**

- should use arithmetic operator `=` replace `+=` in [_totalSupply += amount](solidity/token_fallback_test.sol.sol#L149)
- should use arithmetic operator `=` replace `+=` in [balance += msg.value](solidity/token_fallback_test.sol.sol#L225)
- should use arithmetic operator `=` replace `+=` in [balance += msg.value](solidity/token_fallback_test.sol.sol#L229)

### recommendation
Using arithmetic operator `=` replace assignment operator `+=` or `-=` 

### locations
- solidity/token_fallback_test.sol.sol#L149
- solidity/token_fallback_test.sol.sol#L225
- solidity/token_fallback_test.sol.sol#L229

### severity
Optimization

### category
assignment-left-operation

### confidence
High

## [Optimization] `internal` functions only called once can be inlined to save gas

### description

Not inlining costs **20 to 40 gas** because of two extra `JUMP` instructions and additional stack operations needed for function calls.
more detail see [this](https://docs.soliditylang.org/en/v0.8.20/internals/optimizer.html#function-inlining) and [this](https://blog.soliditylang.org/2021/03/02/saving-gas-with-simple-inliner/)
        

**There is `1` instance of this issue:**

- [ERC20._mint(address,uint256)](solidity/token_fallback_test.sol.sol#L144-L154) could be inlined to save gas.


### recommendation
Using inlining replace `internal` function which only called once

### locations
- solidity/token_fallback_test.sol.sol#L144-L154

### severity
Optimization

### category
internal-function-to-inline

### confidence
High

## [Optimization] Using custom errors replace `require` or `assert`

### description

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `9` instances of this issue:**

- [require(bool,string)(currentAllowance >= amount,"ERC20: transfer amount exceeds allowance")](solidity/token_fallback_test.sol.sol#L99) should use custom error to save gas.

- [require(bool,string)(currentAllowance >= subtractedValue,"ERC20: decreased allowance below zero")](solidity/token_fallback_test.sol.sol#L114) should use custom error to save gas.

- [require(bool,string)(sender != address(0),"ERC20: transfer from the zero address")](solidity/token_fallback_test.sol.sol#L127) should use custom error to save gas.

- [require(bool,string)(recipient != address(0),"ERC20: transfer to the zero address")](solidity/token_fallback_test.sol.sol#L128) should use custom error to save gas.

- [require(bool,string)(senderBalance >= amount,"ERC20: transfer amount exceeds balance")](solidity/token_fallback_test.sol.sol#L133) should use custom error to save gas.

- [require(bool,string)(account != address(0),"ERC20: mint to the zero address")](solidity/token_fallback_test.sol.sol#L145) should use custom error to save gas.

- [require(bool,string)(owner != address(0),"ERC20: approve from the zero address")](solidity/token_fallback_test.sol.sol#L161) should use custom error to save gas.

- [require(bool,string)(spender != address(0),"ERC20: approve to the zero address")](solidity/token_fallback_test.sol.sol#L162) should use custom error to save gas.

- [require(bool,string)(sent,"Failed!")](solidity/token_fallback_test.sol.sol#L216) should use custom error to save gas.


### recommendation

Using custom errors replace `require` or `assert`.


### locations
- solidity/token_fallback_test.sol.sol#L99
- solidity/token_fallback_test.sol.sol#L114
- solidity/token_fallback_test.sol.sol#L127
- solidity/token_fallback_test.sol.sol#L128
- solidity/token_fallback_test.sol.sol#L133
- solidity/token_fallback_test.sol.sol#L145
- solidity/token_fallback_test.sol.sol#L161
- solidity/token_fallback_test.sol.sol#L162
- solidity/token_fallback_test.sol.sol#L216

### severity
Optimization

### category
use-custom-error

### confidence
High

## [Optimization] Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead

### description

> When using elements that are smaller than 32 bytes, your contract’s gas usage may be higher. This is because the EVM operates on 32 bytes at a time. Therefore, if the element is smaller than that, the EVM must use more operations in order to reduce the size of the element from 32 bytes to the desired size.

More detail see [this.](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html)

Each operation involving a `uint8` costs an extra [**22-28 gas**](https://gist.github.com/0xxfu/3672fec07eb3031cd5da14ac015e04a1) (depending on whether the other operand is also a variable of type `uint8`) as compared to ones involving `uint256`, due to the compiler having to clear the higher bits of the memory word before operating on the `uint8`, as well as the associated stack operations of doing so. Use a larger size then downcast where needed


**There are `2` instances of this issue:**

- `uint8 `[IERC20Metadata.decimals().](solidity/token_fallback_test.sol.sol#L39) should be used `uint256/int256`.

- `uint8 `[ERC20.decimals().](solidity/token_fallback_test.sol.sol#L65) should be used `uint256/int256`.


### recommendation

Using `uint256/int256` replace `uint128/uint64/uint32/uint16/uint8` or `int128/int64/int32/int16/int8`


### locations
- solidity/token_fallback_test.sol.sol#L39
- solidity/token_fallback_test.sol.sol#L65

### severity
Optimization

### category
smaller-uint-int

### confidence
High

## [Optimization] Remove unused parameter variables

### description

Unused parameters variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 



**There are `2` instances of this issue:**

- The param variables in [ERC20._beforeTokenTransfer(address,address,uint256)](solidity/token_fallback_test.sol.sol#L168-L172) are unused.
	- [ERC20._beforeTokenTransfer(address,address,uint256).from](solidity/token_fallback_test.sol.sol#L169)
	- [ERC20._beforeTokenTransfer(address,address,uint256).to](solidity/token_fallback_test.sol.sol#L170)
	- [ERC20._beforeTokenTransfer(address,address,uint256).amount](solidity/token_fallback_test.sol.sol#L171)

- The param variables in [ERC20._afterTokenTransfer(address,address,uint256)](solidity/token_fallback_test.sol.sol#L174-L178) are unused.
	- [ERC20._afterTokenTransfer(address,address,uint256).from](solidity/token_fallback_test.sol.sol#L175)
	- [ERC20._afterTokenTransfer(address,address,uint256).to](solidity/token_fallback_test.sol.sol#L176)
	- [ERC20._afterTokenTransfer(address,address,uint256).amount](solidity/token_fallback_test.sol.sol#L177)


### recommendation

Remove the unused parameter variables.


### locations
- solidity/token_fallback_test.sol.sol#L168-L172
- solidity/token_fallback_test.sol.sol#L174-L178

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


**There is `1` instance of this issue:**

- The local variables in [AmazoniumToken.Distribute()](solidity/token_fallback_test.sol.sol#L212-L217) are unused.
	- [AmazoniumToken.Distribute().ownerBalance](solidity/token_fallback_test.sol.sol#L213)


### recommendation

Remove the unused local variables.


### locations
- solidity/token_fallback_test.sol.sol#L212-L217

### severity
Optimization

### category
unused-local-var

### confidence
High

## [Optimization] The result of function calls should be cached rather than re-calling the function

### description

The instances below point to the second+ call of the function within a single function


**There are `3` instances of this issue:**

- `Context._msgSender()` called result should be cached with local variable in [ERC20.transferFrom(address,address,uint256)](solidity/token_fallback_test.sol.sol#L91-L105), It is called more than once:
	- [currentAllowance = _allowances[sender][_msgSender()]](solidity/token_fallback_test.sol.sol#L98)
	- [_approve(sender,_msgSender(),currentAllowance - amount)](solidity/token_fallback_test.sol.sol#L101)

- `Context._msgSender()` called result should be cached with local variable in [ERC20.decreaseAllowance(address,uint256)](solidity/token_fallback_test.sol.sol#L112-L120), It is called more than once:
	- [currentAllowance = _allowances[_msgSender()][spender]](solidity/token_fallback_test.sol.sol#L113)
	- [_approve(_msgSender(),spender,currentAllowance - subtractedValue)](solidity/token_fallback_test.sol.sol#L116)

- `ERC20.totalSupply()` called result should be cached with local variable in [AmazoniumToken.constructor()](solidity/token_fallback_test.sol.sol#L207-L211), It is called more than once:
	- [_approve(address(this),msg.sender,totalSupply())](solidity/token_fallback_test.sol.sol#L209)
	- [_transfer(address(this),msg.sender,totalSupply())](solidity/token_fallback_test.sol.sol#L210)


### recommendation

Using local variable to cache function called result if the same function called more than once.


### locations
- solidity/token_fallback_test.sol.sol#L91-L105
- solidity/token_fallback_test.sol.sol#L112-L120
- solidity/token_fallback_test.sol.sol#L207-L211

### severity
Optimization

### category
cache-call-function-result

### confidence
High

## [Optimization] Dead-code: functions not used should be removed to save deployment gas

### description
Functions that are not sued.

**There is `1` instance of this issue:**

- [Context._msgData()](solidity/token_fallback_test.sol.sol#L10-L12) is never used and should be removed


### recommendation
Remove unused functions.

### locations
- solidity/token_fallback_test.sol.sol#L10-L12

### severity
Optimization

### category
dead-code

### confidence
High

## [Optimization] Use indexed events for value types as they are less costly compared to non-indexed ones

### description

Using the `indexed` keyword for [value types](https://docs.soliditylang.org/en/v0.8.20/types.html#value-types) (`bool/int/address/string/bytes`) saves gas costs, as seen in [this example](https://gist.github.com/0xxfu/c292a65ecb61cae6fd2090366ea0877e).

However, this is only the case for value types, whereas indexing [reference types](https://docs.soliditylang.org/en/v0.8.20/types.html#reference-types) (`array/struct`) are more expensive than their unindexed version.


**There are `2` instances of this issue:**

- The following variables should be indexed in [IERC20.Transfer(address,address,uint256)](solidity/token_fallback_test.sol.sol#L29):

	- [value](solidity/token_fallback_test.sol.sol#L29)

- The following variables should be indexed in [IERC20.Approval(address,address,uint256)](solidity/token_fallback_test.sol.sol#L30):

	- [value](solidity/token_fallback_test.sol.sol#L30)


### recommendation

Using the `indexed` keyword for values types `bool/int/address/string/bytes` in event


### locations
- solidity/token_fallback_test.sol.sol#L29
- solidity/token_fallback_test.sol.sol#L30

### severity
Optimization

### category
unindexed-event

### confidence
High

## [Optimization] Amounts should be checked for `0` before calling a `transfer`

### description

According to the fact that EIP-20 [states](https://github.com/ethereum/EIPs/blob/46b9b698815abbfa628cd1097311deee77dd45c5/EIPS/eip-20.md?plain=1#L116) that zero-valued transfers must be accepted.

Checking non-zero transfer values can avoid an expensive external call and save gas.
While this is done at some places, it’s not consistently done in the solution.


**There is `1` instance of this issue:**

- Adding a non-zero-value check for [badToken.transfer(distAddr,BadTokenBalance)](solidity/token_fallback_test.sol.sol#L221) at the beginning of [AmazoniumToken.purgeBadToken(IERC20)](solidity/token_fallback_test.sol.sol#L219-L222)


### recommendation

Consider adding a non-zero-value check at the beginning of function.


### locations
- solidity/token_fallback_test.sol.sol#L221

### severity
Optimization

### category
zero-check-with-transfer

### confidence
High

## [Optimization] Use assembly to check for `address(0)`

### description

[Inline Assembly](https://docs.soliditylang.org/en/latest/assembly.html) more gas efficient and [Saving Gas with Simple Inlining](https://blog.soliditylang.org/2021/03/02/saving-gas-with-simple-inliner/).



**There are `5` instances of this issue:**

- [require(bool,string)(sender != address(0),"ERC20: transfer from the zero address")](solidity/token_fallback_test.sol.sol#L127) should use assembly to check for `address(0)`

- [require(bool,string)(recipient != address(0),"ERC20: transfer to the zero address")](solidity/token_fallback_test.sol.sol#L128) should use assembly to check for `address(0)`

- [require(bool,string)(account != address(0),"ERC20: mint to the zero address")](solidity/token_fallback_test.sol.sol#L145) should use assembly to check for `address(0)`

- [require(bool,string)(owner != address(0),"ERC20: approve from the zero address")](solidity/token_fallback_test.sol.sol#L161) should use assembly to check for `address(0)`

- [require(bool,string)(spender != address(0),"ERC20: approve to the zero address")](solidity/token_fallback_test.sol.sol#L162) should use assembly to check for `address(0)`


### recommendation

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


### locations
- solidity/token_fallback_test.sol.sol#L127
- solidity/token_fallback_test.sol.sol#L128
- solidity/token_fallback_test.sol.sol#L145
- solidity/token_fallback_test.sol.sol#L161
- solidity/token_fallback_test.sol.sol#L162

### severity
Optimization

### category
zero-address-optimization

### confidence
High

## [Optimization] Setting the constructor to `payable`

### description

You can cut out 10 opcodes in the creation-time EVM bytecode 
if you declare a constructor `payable`. 
Making the constructor `payable` eliminates the need for an initial check 
of `msg.value == 0` and saves `13 gas` on deployment with no security risks.


**There are `3` instances of this issue:**

- [ERC20.constructor(string,string)](solidity/token_fallback_test.sol.sol#L52-L55) should be set to `payable` 

- [Ownable.constructor()](solidity/token_fallback_test.sol.sol#L186-L188) should be set to `payable` 

- [AmazoniumToken.constructor()](solidity/token_fallback_test.sol.sol#L207-L211) should be set to `payable` 


### recommendation

Set the constructor to `payable`.


### locations
- solidity/token_fallback_test.sol.sol#L52-L55
- solidity/token_fallback_test.sol.sol#L186-L188
- solidity/token_fallback_test.sol.sol#L207-L211

### severity
Optimization

### category
payable-constructor

### confidence
High

## [Optimization] Functions guaranteed to revert when called by normal users can be marked `payable`

### description

If a function modifier such as `onlyOwner/onlyAdmin/only**` is used, 
the function will revert if a normal user tries to pay the function. 
Marking the function as payable will lower the gas cost for legitimate callers 
because the compiler will not include checks for whether a payment was provided. 

The extra opcodes avoided are `CALLVALUE(2)`,`DUP1(3)`,`ISZERO(3)`,`PUSH2(3)`,
`JUMPI(10)`,`PUSH1(3)`,`DUP1(3)`,`REVERT(0)`,`JUMPDEST(1)`,`POP(2)`, 
which costs an average of about `21 gas` per call to the function, 
in addition to the extra deployment cost


**There are `2` instances of this issue:**

- [AmazoniumToken.Distribute()](solidity/token_fallback_test.sol.sol#L212-L217) should be set to `payable` 

- [AmazoniumToken.purgeBadToken(IERC20)](solidity/token_fallback_test.sol.sol#L219-L222) should be set to `payable` 


### recommendation

Set the function to `payable`.


### locations
- solidity/token_fallback_test.sol.sol#L212-L217
- solidity/token_fallback_test.sol.sol#L219-L222

### severity
Optimization

### category
payable-function

### confidence
High

## [Optimization] Shortening revert strings to fit in 32 `bytes`

### description

In Solidity, the size of a string is not fixed and depends on the length of the string. 
Each character in a string requires 2 `bytes` of storage. 
Additionally, there is an overhead of 32 `bytes` to store the length of the string.

Shortening revert strings to fit in 32 bytes will decrease deployment time gas 
and will decrease runtime gas when the revert condition is met.


**There are `7` instances of this issue:**

- [require(bool,string)(currentAllowance >= amount,"ERC20: transfer amount exceeds allowance")](solidity/token_fallback_test.sol.sol#L99) should be shortened strings to fit in 32 `bytes` (16 characters).

- [require(bool,string)(currentAllowance >= subtractedValue,"ERC20: decreased allowance below zero")](solidity/token_fallback_test.sol.sol#L114) should be shortened strings to fit in 32 `bytes` (16 characters).

- [require(bool,string)(sender != address(0),"ERC20: transfer from the zero address")](solidity/token_fallback_test.sol.sol#L127) should be shortened strings to fit in 32 `bytes` (16 characters).

- [require(bool,string)(recipient != address(0),"ERC20: transfer to the zero address")](solidity/token_fallback_test.sol.sol#L128) should be shortened strings to fit in 32 `bytes` (16 characters).

- [require(bool,string)(senderBalance >= amount,"ERC20: transfer amount exceeds balance")](solidity/token_fallback_test.sol.sol#L133) should be shortened strings to fit in 32 `bytes` (16 characters).

- [require(bool,string)(owner != address(0),"ERC20: approve from the zero address")](solidity/token_fallback_test.sol.sol#L161) should be shortened strings to fit in 32 `bytes` (16 characters).

- [require(bool,string)(spender != address(0),"ERC20: approve to the zero address")](solidity/token_fallback_test.sol.sol#L162) should be shortened strings to fit in 32 `bytes` (16 characters).


### recommendation

Shortening revert strings to fit in 32 `bytes`


### locations
- solidity/token_fallback_test.sol.sol#L99
- solidity/token_fallback_test.sol.sol#L114
- solidity/token_fallback_test.sol.sol#L127
- solidity/token_fallback_test.sol.sol#L128
- solidity/token_fallback_test.sol.sol#L133
- solidity/token_fallback_test.sol.sol#L161
- solidity/token_fallback_test.sol.sol#L162

### severity
Optimization

### category
revert-long-strings

### confidence
High

## [Optimization] Use `assembly` to write address storage values

### description

Where it does not affect readability, 
using assembly for simple setters allows to save gas not only on deployment, 
but also on function calls.


**There is `1` instance of this issue:**

- [_owner = msg.sender](solidity/token_fallback_test.sol.sol#L187) should use `assembly` update address to save gas.


### recommendation

Using `assembly` update address to save gas.

For example:
```
contract Contract1 {
    address owner;

    function assemblyUpdateOwner(address newOwner) public {
        assembly {
            sstore(owner.slot, newOwner)
        }
    }
}
```


### locations
- solidity/token_fallback_test.sol.sol#L187

### severity
Optimization

### category
assembly-update-address

### confidence
High

## [Optimization] Empty blocks should be removed or emit something

### description

The code should be refactored such that they no longer exist, or the block should do 
something useful, such as emitting an event or reverting. 
If the contract is meant to be extended, the contract should be `abstract` and the function 
signatures be added without any default implementation.


**There are `2` instances of this issue:**

- [ERC20._beforeTokenTransfer(address,address,uint256)](solidity/token_fallback_test.sol.sol#L168-L172) should removed or do something

- [ERC20._afterTokenTransfer(address,address,uint256)](solidity/token_fallback_test.sol.sol#L174-L178) should removed or do something


### recommendation

Empty blocks should emit an event, or revert. 
If not, they can simply be removed to save gas upon deployment. 
This is valid for `receive()` functions, but also `constructors()`


### locations
- solidity/token_fallback_test.sol.sol#L168-L172
- solidity/token_fallback_test.sol.sol#L174-L178

### severity
Optimization

### category
empty-block

### confidence
High

## [Optimization] Use `selfbalance()` instead of `address(this).balance`

### description

You can use `selfbalance()` instead of `address(this).balance` when 
getting your contract’s balance of ETH to save gas. 
Additionally, you can use `balance(address)` instead of address.balance() when 
getting an external contract’s balance of ETH.


**There are `2` instances of this issue:**

- Should use `selfbalance()` instead of [ownerBalance = address(this).balance](solidity/token_fallback_test.sol.sol#L213)

- Should use `selfbalance()` instead of [(sent,None) = address(distAddr).call{value: address(this).balance}("")](solidity/token_fallback_test.sol.sol#L214)


### recommendation

Using `selfbalance()` instead of `address(this).balance`, for example:

```
function assemblyInternalBalance() public returns (uint256) {
    assembly {
        let c := selfbalance()
        mstore(0x00, c)
        return(0x00, 0x20)
    }
}
```


### locations
- solidity/token_fallback_test.sol.sol#L213
- solidity/token_fallback_test.sol.sol#L214

### severity
Optimization

### category
use-self-balance

### confidence
High

## [Optimization] Use `delete` to Clear Variables

### description

delete a assigns the initial value for the type to a. i.e. 
for integers it is equivalent to a = 0, but it can also be used on arrays, 
where it assigns a dynamic array of length zero or a static array of the same 
length with all elements reset. For structs, it assigns a struct with all members reset. 
Similarly, it can also be used to set an address to zero address. 
It has no effect on whole mappings though (as the keys of mappings may be arbitrary 
and are generally unknown). However, individual keys and what they map to can be deleted: 
If a is a mapping, then delete a[x] will delete the value stored at x.

The delete key better conveys the intention and is also more idiomatic. 
Consider replacing assignments of zero with delete statements.


**There is `1` instance of this issue:**

- Should use `delete` statement instead of [ownerBalance = 0](solidity/token_fallback_test.sol.sol#L215)


### recommendation

Replacing assignments of zero with delete statements.



### locations
- solidity/token_fallback_test.sol.sol#L215

### severity
Optimization

### category
use-delete-statement

### confidence
High

## [Optimization] State variables that could be declared constant

### description
State variables that are not updated following deployment should be declared constant to save gas.

**There is `1` instance of this issue:**

- [AmazoniumToken.distAddr](solidity/token_fallback_test.sol.sol#L205) should be constant 


### recommendation
Add the `constant` attribute to state variables that never change.

### locations
- solidity/token_fallback_test.sol.sol#L205

### severity
Optimization

### category
constable-states

### confidence
High

## [Optimization] State variables that could be declared constant

### description
Constant state variables should be declared constant to save gas.

**There is `1` instance of this issue:**

- [AmazoniumToken.distAddr](solidity/token_fallback_test.sol.sol#L205) should be constant


### recommendation
Add the `constant` attributes to state variables that never change.

### locations
- solidity/token_fallback_test.sol.sol#L205

### severity
Optimization

### category
state-should-be-constant

### confidence
High
