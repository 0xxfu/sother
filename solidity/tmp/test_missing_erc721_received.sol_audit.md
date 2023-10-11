## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Unsafe use of `transfer()/transferFrom()` with IERC20 | 4 |
| [M-1] | Using `ERC721.transferFrom()` may cause the user's NFT to be frozen in a contract that does not support ERC721 | 2 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | `onERC721Received` not implemented in ERC721 received contract | 1 |
| [L-1] | `onERC721Received` callback is never called when new tokens are minted or transferred | 3 |
| [L-2] | Missing Event Setter | 12 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Assembly usage | 2 |
| [N-2] | Missing inheritance | 1 |



## [Medium] Unsafe use of `transfer()/transferFrom()` with IERC20

### description

Some tokens do not implement the ERC20 standard properly but are still accepted by most code 
that accepts ERC20 tokens. For example Tether (USDT)'s `transfer()` and `transferFrom()` functions 
on L1 do not return booleans as the specification requires, and instead have no return value. 
When these sorts of tokens are cast to IERC20, their [function signatures](https://medium.com/coinmonks/missing-return-value-bug-at-least-130-tokens-affected-d67bf08521ca) 
do not match and therefore the calls made, revert.


**There are `4` instances of this issue:**

- [token.transferFrom(msg.sender,address(this),tokenId)](solidity/tmp/test_missing_erc721_received.sol#L37) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [token.transferFrom(msg.sender,address(this),tokenId)](solidity/tmp/test_missing_erc721_received.sol#L56) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [token.transferFrom(address(this),msg.sender,tokenId)](solidity/tmp/test_missing_erc721_received.sol#L84) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [token.transferFrom(address(this),msg.sender,tokenId)](solidity/tmp/test_missing_erc721_received.sol#L136) should be replaced by `safeTransfer()/safeTransferFrom()`.


### recommendation

Use [OpenZeppelin’s SafeERC20](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol) 
`safeTransfer()/safeTransferFrom()` instead of `transfer()/transferFrom()`


### locations
- solidity/tmp/test_missing_erc721_received.sol#L37
- solidity/tmp/test_missing_erc721_received.sol#L56
- solidity/tmp/test_missing_erc721_received.sol#L84
- solidity/tmp/test_missing_erc721_received.sol#L136

### severity
Medium

### category
unsafe-transfer

### confidence
High

## [Medium] Using `ERC721.transferFrom()` may cause the user's NFT to be frozen in a contract that does not support ERC721

### description

ERC721 NFTs may get locked forever if the recipient is not aware of ERC721 for some reason. 
While `safeTransferFrom()` is used for ERC1155 NFTs (which has the `_doSafeTransferAcceptanceCheck` 
check on recipient and does not have an option to avoid this), `transferFrom()` is used for 
ERC721 NFTs presumably for gas savings and reentrancy concerns over its `safeTransferFrom` 
variant (which has the `_checkOnERC721Received` check on the recipient).


**There are `2` instances of this issue:**

- [token.transferFrom(address(this),msg.sender,tokenId)](solidity/tmp/test_missing_erc721_received.sol#L84) should be replaced by `safeTransferFrom()`.

- [token.transferFrom(address(this),msg.sender,tokenId)](solidity/tmp/test_missing_erc721_received.sol#L136) should be replaced by `safeTransferFrom()`.

#### Exploit scenario

if `_to` is a contract address that does not support ERC721, the NFT can be frozen in 
that contract.

As per the documentation of EIP-721:
> A wallet/broker/auction application MUST implement the wallet interface if it will 
accept safe transfers.

Ref: https://eips.ethereum.org/EIPS/eip-721


### recommendation

Evaluate using ERC721 `safeTransferFrom()` to avoid NFTs getting stuck vis-a-vis its 
reentrancy risk and gas costs.


### locations
- solidity/tmp/test_missing_erc721_received.sol#L84
- solidity/tmp/test_missing_erc721_received.sol#L136

### severity
Medium

### category
unsafe-721-transfer

### confidence
Medium

## [Low] `onERC721Received` not implemented in ERC721 received contract

### description

The contract does not implement the `onERC721Received` function, 
which is considered a best practice to transfer ERC721 tokens from contracts to contracts. 
The absence of this function could prevent the contract from receiving ERC721 tokens 
from other contracts via `safeTransferFrom/transferFrom`.


**There is `1` instance of this issue:**

- [BadMissReceived](solidity/tmp/test_missing_erc721_received.sol#L22-L39) received NFT via following operations is missing `onERC721Received` function: 
	- [token.transferFrom(msg.sender,address(this),tokenId)](solidity/tmp/test_missing_erc721_received.sol#L37)
	- [token.safeTransferFrom(msg.sender,address(this),tokenId,new bytes(32))](solidity/tmp/test_missing_erc721_received.sol#L24-L29)
	- [token.safeTransferFrom(msg.sender,address(this),tokenId)](solidity/tmp/test_missing_erc721_received.sol#L33)


### recommendation

Consider adding an implementation of the `onERC721Received` function in the contract.


### locations
- solidity/tmp/test_missing_erc721_received.sol#L22-L39

### severity
Low

### category
missing-erc721-received

### confidence
High

## [Low] `onERC721Received` callback is never called when new tokens are minted or transferred

### description

The ERC721 implementation used by the contract does not properly call the
corresponding callback when new tokens are minted or transferred.

The [ERC721 standard](https://eips.ethereum.org/EIPS/eip-721) states that the onERC721Received callback must be called when a
mint or transfer operation occurs.

However, the smart contracts interacting as users of the contracts will not be
notified with the `onERC721Received` callback, as expected according to the ERC721
standard.


**There are `3` instances of this issue:**

- [token.safeTransferFrom(address(this),msg.sender,tokenId,new bytes(32))](solidity/tmp/test_missing_erc721_received.sol#L71-L76) unchecked `onERC721Received` callback.

- [token.safeTransferFrom(address(this),msg.sender,tokenId)](solidity/tmp/test_missing_erc721_received.sol#L80) unchecked `onERC721Received` callback.

- [token.transferFrom(address(this),msg.sender,tokenId)](solidity/tmp/test_missing_erc721_received.sol#L84) unchecked `onERC721Received` callback.

#### Exploit scenario

Alice deploys a contract to interact with the Controller contract to send and receive
ERC721 tokens. Her contract correctly implements the `onERC71Received` callback, but this
is not called when tokens are minted or transferred back to her contract. As a result, the
tokens are trapped.


### recommendation

Short term, ensure that the ERC721 implementations execute the standard callback when
they are required.

Example see OpenZeppelin implementation: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/8b72e20e326078029b92d526ff5a44add2671df1/contracts/token/ERC721/ERC721.sol#L425-L447


### locations
- solidity/tmp/test_missing_erc721_received.sol#L71-L76
- solidity/tmp/test_missing_erc721_received.sol#L80
- solidity/tmp/test_missing_erc721_received.sol#L84

### severity
Low

### category
unchecked-erc721-received

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `12` instances of this issue:**

- Setter function [BadMissReceived.deposit(IERC721,uint256)](solidity/tmp/test_missing_erc721_received.sol#L23-L30) does not emit an event

- Setter function [BadMissReceived.deposit2(IERC721,uint256)](solidity/tmp/test_missing_erc721_received.sol#L32-L34) does not emit an event

- Setter function [BadMissReceived.deposit3(IERC721,uint256)](solidity/tmp/test_missing_erc721_received.sol#L36-L38) does not emit an event

- Setter function [NotBad.deposit(IERC721,uint256)](solidity/tmp/test_missing_erc721_received.sol#L42-L49) does not emit an event

- Setter function [NotBad.deposit2(IERC721,uint256)](solidity/tmp/test_missing_erc721_received.sol#L51-L53) does not emit an event

- Setter function [NotBad.deposit3(IERC721,uint256)](solidity/tmp/test_missing_erc721_received.sol#L55-L57) does not emit an event

- Setter function [BadUnchecked.deposit(IERC721,uint256)](solidity/tmp/test_missing_erc721_received.sol#L70-L77) does not emit an event

- Setter function [BadUnchecked.deposit2(IERC721,uint256)](solidity/tmp/test_missing_erc721_received.sol#L79-L81) does not emit an event

- Setter function [BadUnchecked.deposit3(IERC721,uint256)](solidity/tmp/test_missing_erc721_received.sol#L83-L85) does not emit an event

- Setter function [NotBadChecked.deposit(IERC721,uint256)](solidity/tmp/test_missing_erc721_received.sol#L98-L126) does not emit an event

- Setter function [NotBadChecked.deposit2(IERC721,uint256)](solidity/tmp/test_missing_erc721_received.sol#L128-L133) does not emit an event

- Setter function [NotBadChecked.deposit3(IERC721,uint256)](solidity/tmp/test_missing_erc721_received.sol#L135-L140) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/test_missing_erc721_received.sol#L23-L30
- solidity/tmp/test_missing_erc721_received.sol#L32-L34
- solidity/tmp/test_missing_erc721_received.sol#L36-L38
- solidity/tmp/test_missing_erc721_received.sol#L42-L49
- solidity/tmp/test_missing_erc721_received.sol#L51-L53
- solidity/tmp/test_missing_erc721_received.sol#L55-L57
- solidity/tmp/test_missing_erc721_received.sol#L70-L77
- solidity/tmp/test_missing_erc721_received.sol#L79-L81
- solidity/tmp/test_missing_erc721_received.sol#L83-L85
- solidity/tmp/test_missing_erc721_received.sol#L98-L126
- solidity/tmp/test_missing_erc721_received.sol#L128-L133
- solidity/tmp/test_missing_erc721_received.sol#L135-L140

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

**There are `2` instances of this issue:**

- [NotBadChecked.deposit(IERC721,uint256)](solidity/tmp/test_missing_erc721_received.sol#L98-L126) uses assembly
	- [INLINE ASM](solidity/tmp/test_missing_erc721_received.sol#L121-L123)

- [NotBadChecked._checkOnERC721Received(address,address,uint256,bytes)](solidity/tmp/test_missing_erc721_received.sol#L142-L170) uses assembly
	- [INLINE ASM](solidity/tmp/test_missing_erc721_received.sol#L162-L164)


### recommendation
Do not use `evm` assembly.

### locations
- solidity/tmp/test_missing_erc721_received.sol#L98-L126
- solidity/tmp/test_missing_erc721_received.sol#L142-L170

### severity
Informational

### category
assembly

### confidence
High

## [Informational] Missing inheritance

### description
Detect missing inheritance.

**There is `1` instance of this issue:**

- [NotBad](solidity/tmp/test_missing_erc721_received.sol#L41-L67) should inherit from [IERC721Receiver](solidity/tmp/test_missing_erc721_received.sol#L88-L95)

#### Exploit scenario

```solidity
interface ISomething {
    function f1() external returns(uint);
}

contract Something {
    function f1() external returns(uint){
        return 42;
    }
}
```
`Something` should inherit from `ISomething`. 


### recommendation
Inherit from the missing interface or contract.

### locations
- solidity/tmp/test_missing_erc721_received.sol#L41-L67

### severity
Informational

### category
missing-inheritance

### confidence
High
