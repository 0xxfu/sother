## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | Arbitrary `from` in transferFrom | 3 |


### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Return values of `transfer()/transferFrom()` not checked | 3 |
| [M-1] | Unsafe use of `transfer()/transferFrom()` with IERC20 | 3 |
| [M-2] | Void function | 1 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Functions calling contracts/addresses with transfer hooks are missing reentrancy guards | 9 |
| [L-1] | Missing Event Setter | 5 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 2 |
| [N-1] | Conformance to Solidity naming conventions | 1 |
| [N-2] | SPDX license Identifier | 1 |
| [N-3] | Unnecessary Public Function Modifier | 4 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | State variables only set in the constructor should be declared immutable | 3 |
| [G-1] | Should use latest solidity version `0.8.21` for gas reduction and improved security. | 1 |
| [G-2] | Remove unused parameter variables | 3 |
| [G-3] | Amounts should be checked for `0` before calling a `transfer` | 9 |
| [G-4] | Setting the constructor to `payable` | 1 |
| [G-5] | Use `assembly` to write address storage values | 3 |
| [G-6] | Empty blocks should be removed or emit something | 1 |



## [High] Arbitrary `from` in transferFrom

### description
Detect when `msg.sender` is not used as `from` in transferFrom.

**There are `3` instances of this issue:**

- [C.bad1(address,uint256)](solidity/tmp/send_erc20.sol#L35-L37) uses arbitrary from in transferFrom: [erc20.transferFrom(notsend,to,am)](solidity/tmp/send_erc20.sol#L36)

- [C.bad3(address,address,uint256)](solidity/tmp/send_erc20.sol#L57-L59) uses arbitrary from in transferFrom: [erc20.safeTransferFrom(from,to,amount)](solidity/tmp/send_erc20.sol#L58)

- [C.bad4(address,address,uint256)](solidity/tmp/send_erc20.sol#L65-L67) uses arbitrary from in transferFrom: [SafeERC20.safeTransferFrom(erc20,from,to,amount)](solidity/tmp/send_erc20.sol#L66)

#### Exploit scenario

```solidity
    function a(address from, address to, uint256 amount) public {
        erc20.transferFrom(from, to, am);
    }
```
Alice approves this contract to spend her ERC20 tokens. Bob can call `a` and specify Alice's address as the `from` parameter in `transferFrom`, allowing him to transfer Alice's tokens to himself.

### recommendation

Use `msg.sender` as `from` in transferFrom.


### locations
- solidity/tmp/send_erc20.sol#L35-L37
- solidity/tmp/send_erc20.sol#L57-L59
- solidity/tmp/send_erc20.sol#L65-L67

### severity
High

### category
arbitrary-send-erc20

### confidence
High

## [Medium] Return values of `transfer()/transferFrom()` not checked

### description

Not all `IERC20` implementations `revert()` when there's a failure in `transfer()`/`transferFrom()`. The function signature has a `boolean` return value and they indicate errors that way instead. By not checking the return value, operations that should have marked as failed, may potentially go through without actually making a payment.


**There are `3` instances of this issue:**

- [C.good1(address,uint256)](solidity/tmp/send_erc20.sol#L30-L33) ignores return value by [erc20.transferFrom(from_msgsender,to,am)](solidity/tmp/send_erc20.sol#L32)

- [C.bad1(address,uint256)](solidity/tmp/send_erc20.sol#L35-L37) ignores return value by [erc20.transferFrom(notsend,to,am)](solidity/tmp/send_erc20.sol#L36)

- [C.int_transferFrom(address,address,uint256)](solidity/tmp/send_erc20.sol#L49-L51) ignores return value by [erc20.transferFrom(from,to,amount)](solidity/tmp/send_erc20.sol#L50)

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
- solidity/tmp/send_erc20.sol#L30-L33
- solidity/tmp/send_erc20.sol#L35-L37
- solidity/tmp/send_erc20.sol#L49-L51

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


**There are `3` instances of this issue:**

- [erc20.transferFrom(from_msgsender,to,am)](solidity/tmp/send_erc20.sol#L32) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [erc20.transferFrom(notsend,to,am)](solidity/tmp/send_erc20.sol#L36) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [erc20.transferFrom(from,to,amount)](solidity/tmp/send_erc20.sol#L50) should be replaced by `safeTransfer()/safeTransferFrom()`.


### recommendation

Use [OpenZeppelin’s SafeERC20](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol) 
`safeTransfer()/safeTransferFrom()` instead of `transfer()/transferFrom()`


### locations
- solidity/tmp/send_erc20.sol#L32
- solidity/tmp/send_erc20.sol#L36
- solidity/tmp/send_erc20.sol#L50

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

- function:[SafeERC20.safeTransferFrom(IERC20,address,address,uint256)](solidity/tmp/send_erc20.sol#L4)is empty 

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
- solidity/tmp/send_erc20.sol#L4

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


**There are `9` instances of this issue:**

- [erc20.transferFrom(from_msgsender,to,am)](solidity/tmp/send_erc20.sol#L32) should use Reentrancy-Guard.

- [erc20.transferFrom(notsend,to,am)](solidity/tmp/send_erc20.sol#L36) should use Reentrancy-Guard.

- [erc20.transferFrom(from,to,amount)](solidity/tmp/send_erc20.sol#L50) should use Reentrancy-Guard.

- [erc20.safeTransferFrom(msg.sender,to,amount)](solidity/tmp/send_erc20.sol#L54) should use Reentrancy-Guard.

- [erc20.safeTransferFrom(from,to,amount)](solidity/tmp/send_erc20.sol#L58) should use Reentrancy-Guard.

- [SafeERC20.safeTransferFrom(erc20,msg.sender,to,amount)](solidity/tmp/send_erc20.sol#L62) should use Reentrancy-Guard.

- [SafeERC20.safeTransferFrom(erc20,from,to,amount)](solidity/tmp/send_erc20.sol#L66) should use Reentrancy-Guard.

- [SafeERC20.safeTransferFrom(erc20,address(this),to,amount)](solidity/tmp/send_erc20.sol#L70) should use Reentrancy-Guard.

- [erc20.safeTransferFrom(address(this),to,amount)](solidity/tmp/send_erc20.sol#L74) should use Reentrancy-Guard.


### recommendation

Using [Reentrancy-Guard](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/security/ReentrancyGuard.sol#L50C5-L62) 
when calling contracts/addresses with transfer hooks.


### locations
- solidity/tmp/send_erc20.sol#L32
- solidity/tmp/send_erc20.sol#L36
- solidity/tmp/send_erc20.sol#L50
- solidity/tmp/send_erc20.sol#L54
- solidity/tmp/send_erc20.sol#L58
- solidity/tmp/send_erc20.sol#L62
- solidity/tmp/send_erc20.sol#L66
- solidity/tmp/send_erc20.sol#L70
- solidity/tmp/send_erc20.sol#L74

### severity
Low

### category
reentrancy-transfer

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `5` instances of this issue:**

- Setter function [C.constructor()](solidity/tmp/send_erc20.sol#L24-L28) does not emit an event

- Setter function [C.good1(address,uint256)](solidity/tmp/send_erc20.sol#L30-L33) does not emit an event

- Setter function [C.good2(address,uint256)](solidity/tmp/send_erc20.sol#L39-L42) does not emit an event

- Setter function [C.good3(address,uint256)](solidity/tmp/send_erc20.sol#L53-L55) does not emit an event

- Setter function [C.good4(address,uint256)](solidity/tmp/send_erc20.sol#L61-L63) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/send_erc20.sol#L24-L28
- solidity/tmp/send_erc20.sol#L30-L33
- solidity/tmp/send_erc20.sol#L39-L42
- solidity/tmp/send_erc20.sol#L53-L55
- solidity/tmp/send_erc20.sol#L61-L63

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

**There are `2` instances of this issue:**

- Pragma version[0.8.17](solidity/tmp/send_erc20.sol#L1) allows old versions

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
- solidity/tmp/send_erc20.sol#L1
- 

### severity
Informational

### category
solc-version

### confidence
High

## [Informational] Conformance to Solidity naming conventions

### description

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There is `1` instance of this issue:**

- Function [C.int_transferFrom(address,address,uint256)](solidity/tmp/send_erc20.sol#L49-L51) is not in mixedCase


### recommendation
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations
- solidity/tmp/send_erc20.sol#L49-L51

### severity
Informational

### category
naming-convention

### confidence
High

## [Informational] SPDX license Identifier

### description
The source file does not specify SPDX license identifier.

**There is `1` instance of this issue:**

- key[SafeERC20](solidity/tmp/send_erc20.sol#L3-L5) does not specify SPDX license identifier
#### Exploit scenario

    pragma solidity ^0.4.24;

    contract NoLicense {

    function noLicense() public {
    }

    }
    

### recommendation
Consider adding the SPDX license identifier before deployment.

### locations
- solidity/tmp/send_erc20.sol#L3-L5

### severity
Informational

### category
no-license

### confidence
High

## [Informational] Unnecessary Public Function Modifier

### description
Detect the public function which can be replaced with external

**There are `4` instances of this issue:**

- function:[C.good1(address,uint256)](solidity/tmp/send_erc20.sol#L30-L33)is public and can be replaced with external 

- function:[C.bad1(address,uint256)](solidity/tmp/send_erc20.sol#L35-L37)is public and can be replaced with external 

- function:[C.good2(address,uint256)](solidity/tmp/send_erc20.sol#L39-L42)is public and can be replaced with external 

- function:[C.bad2(address,address,uint256)](solidity/tmp/send_erc20.sol#L45-L47)is public and can be replaced with external 

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
- solidity/tmp/send_erc20.sol#L30-L33
- solidity/tmp/send_erc20.sol#L35-L37
- solidity/tmp/send_erc20.sol#L39-L42
- solidity/tmp/send_erc20.sol#L45-L47

### severity
Informational

### category
unnecessary-public-function-modifier

### confidence
High

## [Optimization] State variables only set in the constructor should be declared immutable

### description

Avoids a Gsset (20000 gas) in the constructor, and replaces the first access in each transaction (Gcoldsload - 2100 gas) and each access thereafter (Gwarmacces - 100 gas) with a PUSH32 (3 gas).

While strings are not value types, and therefore cannot be immutable/constant if not hard-coded outside of the constructor, the same behavior can be achieved by making the current contract abstract with virtual functions for the string accessors, and having a child contract override the functions with the hard-coded implementation-specific values.
    

**There are `3` instances of this issue:**

- [C.erc20](solidity/tmp/send_erc20.sol#L20) should be immutable 

- [C.notsend](solidity/tmp/send_erc20.sol#L21) should be immutable 

- [C.send](solidity/tmp/send_erc20.sol#L22) should be immutable 


### recommendation
Add the `immutable` attribute to state variables that never change or are set only in the constructor.

### locations
- solidity/tmp/send_erc20.sol#L20
- solidity/tmp/send_erc20.sol#L21
- solidity/tmp/send_erc20.sol#L22

### severity
Optimization

### category
immutable-states

### confidence
High

## [Optimization] Should use latest solidity version `0.8.21` for gas reduction and improved security.

### description

[Solidity `0.8.21`](https://soliditylang.org/blog/2023/07/19/solidity-0.8.21-release-announcement) has many optimization with compiler and bugfixes, 
please upgrade Solidity to the latest version(`0.8.21`) for gas reduction and improved security.


**There is `1` instance of this issue:**

- pragma solidity version [0.8.17](solidity/tmp/send_erc20.sol#L1) should upgrade to the latest version: 0.8.21

### recommendation
Upgrade solidity version to the latest version: 0.8.21

### locations
- solidity/tmp/send_erc20.sol#L1

### severity
Optimization

### category
upgrade-to-latest

### confidence
High

## [Optimization] Remove unused parameter variables

### description

Unused parameters variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 



**There are `3` instances of this issue:**

- The param variables in [SafeERC20.safeTransferFrom(IERC20,address,address,uint256)](solidity/tmp/send_erc20.sol#L4) are unused.
	- [SafeERC20.safeTransferFrom(IERC20,address,address,uint256).value](solidity/tmp/send_erc20.sol#L4)
	- [SafeERC20.safeTransferFrom(IERC20,address,address,uint256).token](solidity/tmp/send_erc20.sol#L4)
	- [SafeERC20.safeTransferFrom(IERC20,address,address,uint256).from](solidity/tmp/send_erc20.sol#L4)
	- [SafeERC20.safeTransferFrom(IERC20,address,address,uint256).to](solidity/tmp/send_erc20.sol#L4)

- The param variables in [ERC20.transferFrom(address,address,uint256)](solidity/tmp/send_erc20.sol#L12-L14) are unused.
	- [ERC20.transferFrom(address,address,uint256).amount](solidity/tmp/send_erc20.sol#L12)
	- [ERC20.transferFrom(address,address,uint256).to](solidity/tmp/send_erc20.sol#L12)
	- [ERC20.transferFrom(address,address,uint256).from](solidity/tmp/send_erc20.sol#L12)

- The param variables in [C.good6(address,address,uint256)](solidity/tmp/send_erc20.sol#L73-L75) are unused.
	- [C.good6(address,address,uint256).from](solidity/tmp/send_erc20.sol#L73)


### recommendation

Remove the unused parameter variables.


### locations
- solidity/tmp/send_erc20.sol#L4
- solidity/tmp/send_erc20.sol#L12-L14
- solidity/tmp/send_erc20.sol#L73-L75

### severity
Optimization

### category
unused-parameter

### confidence
High

## [Optimization] Amounts should be checked for `0` before calling a `transfer`

### description

According to the fact that EIP-20 [states](https://github.com/ethereum/EIPs/blob/46b9b698815abbfa628cd1097311deee77dd45c5/EIPS/eip-20.md?plain=1#L116) that zero-valued transfers must be accepted.

Checking non-zero transfer values can avoid an expensive external call and save gas.
While this is done at some places, it’s not consistently done in the solution.


**There are `9` instances of this issue:**

- Adding a non-zero-value check for [erc20.transferFrom(from_msgsender,to,am)](solidity/tmp/send_erc20.sol#L32) at the beginning of [C.good1(address,uint256)](solidity/tmp/send_erc20.sol#L30-L33)

- Adding a non-zero-value check for [erc20.transferFrom(notsend,to,am)](solidity/tmp/send_erc20.sol#L36) at the beginning of [C.bad1(address,uint256)](solidity/tmp/send_erc20.sol#L35-L37)

- Adding a non-zero-value check for [erc20.transferFrom(from,to,amount)](solidity/tmp/send_erc20.sol#L50) at the beginning of [C.int_transferFrom(address,address,uint256)](solidity/tmp/send_erc20.sol#L49-L51)

- Adding a non-zero-value check for [erc20.safeTransferFrom(msg.sender,to,amount)](solidity/tmp/send_erc20.sol#L54) at the beginning of [C.good3(address,uint256)](solidity/tmp/send_erc20.sol#L53-L55)

- Adding a non-zero-value check for [erc20.safeTransferFrom(from,to,amount)](solidity/tmp/send_erc20.sol#L58) at the beginning of [C.bad3(address,address,uint256)](solidity/tmp/send_erc20.sol#L57-L59)

- Adding a non-zero-value check for [SafeERC20.safeTransferFrom(erc20,msg.sender,to,amount)](solidity/tmp/send_erc20.sol#L62) at the beginning of [C.good4(address,uint256)](solidity/tmp/send_erc20.sol#L61-L63)

- Adding a non-zero-value check for [SafeERC20.safeTransferFrom(erc20,from,to,amount)](solidity/tmp/send_erc20.sol#L66) at the beginning of [C.bad4(address,address,uint256)](solidity/tmp/send_erc20.sol#L65-L67)

- Adding a non-zero-value check for [SafeERC20.safeTransferFrom(erc20,address(this),to,amount)](solidity/tmp/send_erc20.sol#L70) at the beginning of [C.good5(address,uint256)](solidity/tmp/send_erc20.sol#L69-L71)

- Adding a non-zero-value check for [erc20.safeTransferFrom(address(this),to,amount)](solidity/tmp/send_erc20.sol#L74) at the beginning of [C.good6(address,address,uint256)](solidity/tmp/send_erc20.sol#L73-L75)


### recommendation

Consider adding a non-zero-value check at the beginning of function.


### locations
- solidity/tmp/send_erc20.sol#L32
- solidity/tmp/send_erc20.sol#L36
- solidity/tmp/send_erc20.sol#L50
- solidity/tmp/send_erc20.sol#L54
- solidity/tmp/send_erc20.sol#L58
- solidity/tmp/send_erc20.sol#L62
- solidity/tmp/send_erc20.sol#L66
- solidity/tmp/send_erc20.sol#L70
- solidity/tmp/send_erc20.sol#L74

### severity
Optimization

### category
zero-check-with-transfer

### confidence
High

## [Optimization] Setting the constructor to `payable`

### description

You can cut out 10 opcodes in the creation-time EVM bytecode 
if you declare a constructor `payable`. 
Making the constructor `payable` eliminates the need for an initial check 
of `msg.value == 0` and saves `13 gas` on deployment with no security risks.


**There is `1` instance of this issue:**

- [C.constructor()](solidity/tmp/send_erc20.sol#L24-L28) should be set to `payable` 


### recommendation

Set the constructor to `payable`.


### locations
- solidity/tmp/send_erc20.sol#L24-L28

### severity
Optimization

### category
payable-constructor

### confidence
High

## [Optimization] Use `assembly` to write address storage values

### description

Where it does not affect readability, 
using assembly for simple setters allows to save gas not only on deployment, 
but also on function calls.


**There are `3` instances of this issue:**

- [send = msg.sender](solidity/tmp/send_erc20.sol#L27) should use `assembly` update address to save gas.

- [from_msgsender = msg.sender](solidity/tmp/send_erc20.sol#L31) should use `assembly` update address to save gas.

- [from_msgsender = msg.sender](solidity/tmp/send_erc20.sol#L40) should use `assembly` update address to save gas.


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
- solidity/tmp/send_erc20.sol#L27
- solidity/tmp/send_erc20.sol#L31
- solidity/tmp/send_erc20.sol#L40

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


**There is `1` instance of this issue:**

- [SafeERC20.safeTransferFrom(IERC20,address,address,uint256)](solidity/tmp/send_erc20.sol#L4) should removed or do something


### recommendation

Empty blocks should emit an event, or revert. 
If not, they can simply be removed to save gas upon deployment. 
This is valid for `receive()` functions, but also `constructors()`


### locations
- solidity/tmp/send_erc20.sol#L4

### severity
Optimization

### category
empty-block

### confidence
High
