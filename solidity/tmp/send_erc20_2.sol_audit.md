## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | Arbitrary `from` in transferFrom | 2 |


### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Void function | 1 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Functions calling contracts/addresses with transfer hooks are missing reentrancy guards | 2 |
| [L-1] | Missing Event Setter | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 2 |
| [N-1] | SPDX license Identifier | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Should use latest solidity version `0.8.21` for gas reduction and improved security. | 1 |
| [G-1] | Remove unused parameter variables | 2 |
| [G-2] | Amounts should be checked for `0` before calling a `transfer` | 2 |
| [G-3] | Setting the constructor to `payable` | 1 |
| [G-4] | Use `assembly` to write address storage values | 1 |
| [G-5] | Empty blocks should be removed or emit something | 1 |



## [High] Arbitrary `from` in transferFrom

### description
Detect when `msg.sender` is not used as `from` in transferFrom.

**There are `2` instances of this issue:**

- [C.bad3(address,address,uint256)](solidity/tmp/send_erc20_2.sol#L31-L33) uses arbitrary from in transferFrom: [erc20.safeTransferFrom(from,to,amount)](solidity/tmp/send_erc20_2.sol#L32)

- [C.bad4(address,address,uint256)](solidity/tmp/send_erc20_2.sol#L35-L37) uses arbitrary from in transferFrom: [SafeERC20.safeTransferFrom(erc20,from,to,amount)](solidity/tmp/send_erc20_2.sol#L36)

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
- solidity/tmp/send_erc20_2.sol#L31-L33
- solidity/tmp/send_erc20_2.sol#L35-L37

### severity
High

### category
arbitrary-send-erc20

### confidence
High

## [Medium] Void function

### description
Detect the call to a function that is not implemented

**There is `1` instance of this issue:**

- function:[SafeERC20.safeTransferFrom(IERC20,address,address,uint256)](solidity/tmp/send_erc20_2.sol#L4)is empty 

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
- solidity/tmp/send_erc20_2.sol#L4

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


**There are `2` instances of this issue:**

- [erc20.safeTransferFrom(from,to,amount)](solidity/tmp/send_erc20_2.sol#L32) should use Reentrancy-Guard.

- [SafeERC20.safeTransferFrom(erc20,from,to,amount)](solidity/tmp/send_erc20_2.sol#L36) should use Reentrancy-Guard.


### recommendation

Using [Reentrancy-Guard](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/security/ReentrancyGuard.sol#L50C5-L62) 
when calling contracts/addresses with transfer hooks.


### locations
- solidity/tmp/send_erc20_2.sol#L32
- solidity/tmp/send_erc20_2.sol#L36

### severity
Low

### category
reentrancy-transfer

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There is `1` instance of this issue:**

- Setter function [C.constructor()](solidity/tmp/send_erc20_2.sol#L24-L28) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/send_erc20_2.sol#L24-L28

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

- Pragma version[0.8.17](solidity/tmp/send_erc20_2.sol#L1) allows old versions

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
- solidity/tmp/send_erc20_2.sol#L1
- 

### severity
Informational

### category
solc-version

### confidence
High

## [Informational] SPDX license Identifier

### description
The source file does not specify SPDX license identifier.

**There is `1` instance of this issue:**

- key[SafeERC20](solidity/tmp/send_erc20_2.sol#L3-L5) does not specify SPDX license identifier
#### Exploit scenario

    pragma solidity ^0.4.24;

    contract NoLicense {

    function noLicense() public {
    }

    }
    

### recommendation
Consider adding the SPDX license identifier before deployment.

### locations
- solidity/tmp/send_erc20_2.sol#L3-L5

### severity
Informational

### category
no-license

### confidence
High

## [Optimization] Should use latest solidity version `0.8.21` for gas reduction and improved security.

### description

[Solidity `0.8.21`](https://soliditylang.org/blog/2023/07/19/solidity-0.8.21-release-announcement) has many optimization with compiler and bugfixes, 
please upgrade Solidity to the latest version(`0.8.21`) for gas reduction and improved security.


**There is `1` instance of this issue:**

- pragma solidity version [0.8.17](solidity/tmp/send_erc20_2.sol#L1) should upgrade to the latest version: 0.8.21

### recommendation
Upgrade solidity version to the latest version: 0.8.21

### locations
- solidity/tmp/send_erc20_2.sol#L1

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



**There are `2` instances of this issue:**

- The param variables in [SafeERC20.safeTransferFrom(IERC20,address,address,uint256)](solidity/tmp/send_erc20_2.sol#L4) are unused.
	- [SafeERC20.safeTransferFrom(IERC20,address,address,uint256).token](solidity/tmp/send_erc20_2.sol#L4)
	- [SafeERC20.safeTransferFrom(IERC20,address,address,uint256).from](solidity/tmp/send_erc20_2.sol#L4)
	- [SafeERC20.safeTransferFrom(IERC20,address,address,uint256).value](solidity/tmp/send_erc20_2.sol#L4)
	- [SafeERC20.safeTransferFrom(IERC20,address,address,uint256).to](solidity/tmp/send_erc20_2.sol#L4)

- The param variables in [ERC20.transferFrom(address,address,uint256)](solidity/tmp/send_erc20_2.sol#L12-L14) are unused.
	- [ERC20.transferFrom(address,address,uint256).from](solidity/tmp/send_erc20_2.sol#L12)
	- [ERC20.transferFrom(address,address,uint256).to](solidity/tmp/send_erc20_2.sol#L12)
	- [ERC20.transferFrom(address,address,uint256).amount](solidity/tmp/send_erc20_2.sol#L12)


### recommendation

Remove the unused parameter variables.


### locations
- solidity/tmp/send_erc20_2.sol#L4
- solidity/tmp/send_erc20_2.sol#L12-L14

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


**There are `2` instances of this issue:**

- Adding a non-zero-value check for [erc20.safeTransferFrom(from,to,amount)](solidity/tmp/send_erc20_2.sol#L32) at the beginning of [C.bad3(address,address,uint256)](solidity/tmp/send_erc20_2.sol#L31-L33)

- Adding a non-zero-value check for [SafeERC20.safeTransferFrom(erc20,from,to,amount)](solidity/tmp/send_erc20_2.sol#L36) at the beginning of [C.bad4(address,address,uint256)](solidity/tmp/send_erc20_2.sol#L35-L37)


### recommendation

Consider adding a non-zero-value check at the beginning of function.


### locations
- solidity/tmp/send_erc20_2.sol#L32
- solidity/tmp/send_erc20_2.sol#L36

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

- [C.constructor()](solidity/tmp/send_erc20_2.sol#L24-L28) should be set to `payable` 


### recommendation

Set the constructor to `payable`.


### locations
- solidity/tmp/send_erc20_2.sol#L24-L28

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


**There is `1` instance of this issue:**

- [send = msg.sender](solidity/tmp/send_erc20_2.sol#L27) should use `assembly` update address to save gas.


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
- solidity/tmp/send_erc20_2.sol#L27

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

- [SafeERC20.safeTransferFrom(IERC20,address,address,uint256)](solidity/tmp/send_erc20_2.sol#L4) should removed or do something


### recommendation

Empty blocks should emit an event, or revert. 
If not, they can simply be removed to save gas upon deployment. 
This is valid for `receive()` functions, but also `constructors()`


### locations
- solidity/tmp/send_erc20_2.sol#L4

### severity
Optimization

### category
empty-block

### confidence
High
